from flask import Flask, request, jsonify, Response, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_bcrypt import Bcrypt, generate_password_hash

import routes
from db import db, init_db
from models.app_users import AppUsers


app = Flask(__name__)

app.app_context().push()
bcrypt = Bcrypt(app)

database_host = "127.0.0.1:5432"
database_name = "rise-thrive"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{database_host}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)

def create_all():
  db.create_all()
  print("Querying for default user...")
   
  user_data = db.session.query(AppUsers).filter(AppUsers.email == 'k.haslem@icloud.com').first()

  if user_data == None:
    print("Admin not found! Creating default user...")
    password = ''
    while password == '' or password is None:
        password = input(' Enter a password for Admin:')

    hashed_password = bcrypt.generate_password_hash(password).decode("utf8")

    record = AppUsers('Kray', 'Haslem', "k.haslem@icloud.com", hashed_password, "super-admin")

    db.session.add(record)
    db.session.commit()

  else:
    print("Default user found!")

app.register_blueprint(routes.auth)
app.register_blueprint(routes.app_users)
app.register_blueprint(routes.contestants)

if __name__ == '__main__':
   create_all()
   app.run(debug=True)