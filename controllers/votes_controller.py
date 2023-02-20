from flask import Request, Response, jsonify
from db import db
import os
from dotenv import load_dotenv
from twilio.rest import Client 

from models.votes import Votes, vote_schema, votes_schema
from lib.authenticate import authenticate

load_dotenv()

def vote_add(req:Request) -> Response:
  post_data = req.get_json()
  
  contestant_id = post_data.get("selection")
  identity = str(post_data.get("identity"))

  identity = "".join(filter(str.isdigit, identity))

  if len(identity) == 10:
    identity = "1" + identity

  if len(identity) != 11 and identity[0] != "1":
    return jsonify({"message":"Invalid phone number format."}), 400

  vote_record = db.session.query(Votes).filter(Votes.identity == identity).first()

  if not vote_record:
    vote_record = Votes.get_generic_vote()

  vote_record.identity = identity
  vote_record.contestant_id = contestant_id

  account_sid = os.getenv('TWILIO_ACCOUNT_SID')
  auth_token = os.getenv('TWILIO_AUTH_TOKEN') 
  service_sid = os.getenv('TWILIO_SERVICE_SID') 

  client = Client(account_sid, auth_token) 
  verification_path = f"http://risethrivepitch.com/pages/verification.html?voteId={vote_record.vote_id}"
  try:
    client.messages.create(messaging_service_sid=service_sid, body=f'{verification_path}', to=f'+{identity}') 
  except:
    return jsonify({"message": "Verification SMS failure."}), 400
  
  if vote_record.contestant_id != "":
    db.session.add(vote_record)
    db.session.commit()

    return jsonify({"message":"Vote submitted."}), 200
  else:
    return jsonify({"message":"Selection not recognized"}), 400

@authenticate
def get_votes(req:Request) -> Response:
  all_votes = db.session.query(Votes).all()

  return jsonify(votes_schema.dump(all_votes)), 200

def verify_vote(req:Request, vote_id) -> Response:
  vote_record = db.session.query(Votes).filter(Votes.vote_id == vote_id).first()
  vote_record.verified = True
  
  db.session.commit()
  return jsonify({"message":"Vote verified.", "vote":vote_schema.dump(vote_record)}), 200

@authenticate
def vote_count(req:Request) -> Response:
  vote_records = db.session.query(Votes).filter(Votes.verified == True).order_by(Votes.contestant_id).all()
  results = {}
  contestant = ""

  for vote in vote_records:
    if vote.contestant.name != contestant:
      contestant = vote.contestant.name
      results[contestant] = 0

    results[contestant] = results[contestant] + 1

  return jsonify(results)





