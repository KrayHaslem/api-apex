from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma


class Contestants(db.Model):
    __tablename__= "Contestants"
    contestant_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(), nullable = False)
    description = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, name, description, active):
        self.name = name
        self.description = description
        self.active = active

    def get_generic_contestant():
        return Contestants("", None, True)
    
class ContestantsSchema(ma.Schema):
    class Meta:
        fields = ['contestant_id','name', 'description', "active"]
    
contestant_schema = ContestantsSchema()
contestants_schema = ContestantsSchema(many=True)