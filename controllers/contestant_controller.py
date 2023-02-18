from flask import Request, Response, jsonify
from db import db

from models.contestants import Contestants, contestant_schema, contestants_schema
from lib.authenticate import authenticate
from lib.update_object import update_object


@authenticate
def contestant_add(req:Request) -> Response:
  post_data = req.get_json()

  contestant = Contestants.get_generic_contestant()

  update_object(contestant, post_data)

  db.session.add(contestant)
  db.session.commit()
   
  return jsonify(contestant_schema.dump(contestant)), 200


@authenticate
def contestant_get(req:Request, user_id) -> Response:
  try:
    contestant = db.session.query(Contestants).filter(Contestants.contestant_id == user_id).first()
    return jsonify(contestant_schema.dump(contestant)), 200
  except:
    return jsonify("Contestant not found"), 404

@authenticate
def contestants_get(req:Request) -> Response:
  all_contestants = db.session.query(Contestants).filter(Contestants.active == True).all()
  return jsonify(contestants_schema.dump(all_contestants)), 200

@authenticate
def contestant_upate(req:Request, contestant_id):
  post_data = req.get_json()

  contestant = db.session.query(Contestants).filter(Contestants.contestant_id == contestant_id).first()

  update_object(contestant, post_data)

  db.session.commit()

  return jsonify(contestant_schema.dump(contestant)), 200