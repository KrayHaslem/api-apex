from flask import request, Response, jsonify
from datetime import datetime, timedelta
from models.app_users import AppUsers, AppUsersSchema
from models.auth_tokens import AuthTokens, auth_token_schema
from db import db
from flask_bcrypt import check_password_hash


def auth_token_add(req:request) -> Response:
    if req.content_type == "application/json":
        post_data = req.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        if email == None:
            return jsonify("ERROR: Email Missing"), 400
        if password == None:
            return jsonify("ERROR: Password Missing"), 400

        now_datetime = datetime.utcnow()
        expiration_datetime = datetime.utcnow() + timedelta(hours=12)
        user_data = db.session.query(AppUsers).filter(AppUsers.email == email).first()
        print("user_data : ",user_data)
        if user_data:
            is_password_valid = check_password_hash(user_data.password, password)
            if is_password_valid == False:
                return jsonify("Invalid email/password"), 401

            auth_data = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_data.user_id).first()
            if auth_data is None:
                auth_data = AuthTokens(user_data.user_id, expiration_datetime)
                db.session.add(auth_data)
            else:
                if now_datetime < auth_data.expiration:
                    db.session.delete(auth_data)
                    auth_data = AuthTokens(user_data.user_id, expiration_datetime)
                    db.session.add(auth_data)
                else:
                    auth_data.expiration = expiration_datetime
        else: 
            return jsonify("Invalid email/password"), 401

        db.session.commit()

        return jsonify(auth_token_schema.dump(auth_data))
    else:
        return jsonify("ERROR: Request Must Be Made in JSON Format"), 404