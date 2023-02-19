from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from models.contestants import ContestantsSchema

class Votes(db.Model):
  __tablename__= "Votes"
  vote_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  identity = db.Column(db.String(), nullable=False)
  contestant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Contestants.contestant_id'), nullable=False)
  verified = db.Column(db.Boolean(), nullable=False, default=False)
  contestant = db.relationship('Contestants', backref=db.backref('Votes', lazy=True))

  def __init__(self, identity, contestant_id):
    self.identity = identity
    self.contestant_id = contestant_id 

  def get_generic_vote():
    return Votes("", "")
    
class VotesSchema(ma.Schema):
  class Meta:
    fields = ['vote_id','identity', 'contestant_id', 'verified', 'contestant']
  contestant = ma.fields.Nested(ContestantsSchema(only=('name',)))
    
vote_schema = VotesSchema()
votes_schema = VotesSchema(many=True)