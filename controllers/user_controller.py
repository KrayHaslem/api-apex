from flask import request, jsonify
from db import db

from models.app_users import AppUsers
from lib.authenticate import authenticate

@authenticate
def user_add():
   form = request.form

   fields = ["first_name", "last_name", "email", "password", "role"]
   req_fields = ["first_name", "email"]
   values = []
   
   for field in fields:
      form_value = form.get(field)
      if form_value in req_fields and form_value == " ":
         return jsonify (f'{field} is required field'), 400

      values.append(form_value)
   
   first_name = form.get('first_name')
   last_name = form.get('last_name')
   email = form.get('email')
   password = form.get('password')
   role = form.get('role')

   new_user_record = AppUsers(first_name, last_name, email, password, role)

   db.session.add(new_user_record)
   db.session.commit()
   
   return jsonify('User Added'), 200