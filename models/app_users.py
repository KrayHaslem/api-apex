from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma


class AppUsers(db.Model):
    __tablename__= "AppUsers"
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    role = db.Column(db.String(), default=' user', nullable=False)
    auth = db.relationship('AuthTokens', backref = 'user')

    def __init__(self, first_name, last_name, email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
    
class AppUsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id','first_name', 'last_name', 'email', 'password', 'role']
    
user_schema = AppUsersSchema()
users_schema = AppUsersSchema(many=True)
