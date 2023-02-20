from flask import Flask, request, jsonify, Response, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_cors import CORS
import os
from dotenv import load_dotenv

import routes
from db import db, init_db
from models.app_users import AppUsers

load_dotenv()

app = Flask(__name__)

app.app_context().push()
bcrypt = Bcrypt(app)
CORS(app)


DATABASE_HOST = os.getenv('DATABASE_HOST')
if not DATABASE_HOST:
  raise EnvironmentError('Unable to Find DATABASE_HOST Variable.')

DATABASE_PORT = os.getenv('DATABASE_PORT')
if not DATABASE_PORT:
  raise EnvironmentError('Unable to Find DATABASE_NAME Variable.')

DATABASE_ID = os.getenv('DATABASE_ID')
if not DATABASE_ID:
  raise EnvironmentError('Unable to Find DATABASE_ID Variable.')

DATABASE_USER = os.getenv('DATABASE_USER')
if not DATABASE_USER:
  raise EnvironmentError('Unable to Find DATABASE_USER Variable.')

DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
if not DATABASE_PASSWORD:
  raise EnvironmentError('Unable to Find DATABASE_PASSWORD Variable.')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_ID}'
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
app.register_blueprint(routes.contestants)
app.register_blueprint(routes.votes)

if __name__ == '__main__':
   create_all()
   app.run()