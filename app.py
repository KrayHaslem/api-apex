from flask import Flask

from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_cors import CORS

import os

import routes

from config import database_uri
from db import db, init_db
from models.app_users import AppUsers

load_dotenv()

app = Flask(__name__)

app.app_context().push()
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("APP_DATABASE_URI", database_uri)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)


def create_all():
    db.create_all()
    print('Querying for default user...')

    user_data = db.session.query(AppUsers).filter(AppUsers.email == 'k.haslem@icloud.com').first()

    if user_data == None:
        print('Admin not found! Creating default user...')

        ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
        if not ADMIN_PASSWORD:
            raise EnvironmentError('Unable to Find ADMIN_PASSWORD Variable.')

        hashed_password = bcrypt.generate_password_hash(ADMIN_PASSWORD).decode('utf8')

        record = AppUsers('Kray', 'Haslem', 'k.haslem@icloud.com', hashed_password, 'super-admin')

        db.session.add(record)
        db.session.commit()

    else:
        print('Default user found!')


app.register_blueprint(routes.auth)
app.register_blueprint(routes.app_users)

if __name__ == '__main__':
    create_all()
    app.run()
