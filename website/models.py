from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    colby_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity':'admin',
    }

class Peak(User):
    __mapper_args__ = {
        'polymorphic_identity':'peak',
    }

class Coach(User):
    __mapper_args__ = {
        'polymorphic_identity':'coach',
    }

class Athlete(User):
    __tablename__ = 'athletes'
    
    colby_id = db.Column(db.Integer, db.ForeignKey('users.colby_id'), primary_key=True)
    status = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    class_year = db.Column(db.Integer)
    position = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'athlete',
    }
