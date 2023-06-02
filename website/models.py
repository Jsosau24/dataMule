"""
Jonathan Sosa 
helper_functions.py
may-jun 2023
"""
# models/class on the file (you can look these up and it will take you there)
## User
## Admin
## Peak
## Coach
## Athlete
## Team
## TeamUserAssociation
## Note

# Imports
from . import db
from datetime import datetime
from flask_login import UserMixin

# Databse Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    colby_id = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

    team_associations = db.relationship('TeamUserAssociation', back_populates="user")

class Admin(User):

    __tablename__ = 'admin'
    colby_id = db.Column(db.Integer, db.ForeignKey('users.colby_id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'admin',
    }

class Peak(User):

    __tablename__ = 'peak'
    colby_id = db.Column(db.Integer, db.ForeignKey('users.colby_id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'peak',
    }

class Coach(User):

    __tablename__ = 'coaches'
    colby_id = db.Column(db.Integer, db.ForeignKey('users.colby_id'), primary_key=True)
    
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

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    team_associations = db.relationship('TeamUserAssociation', back_populates="team")

class TeamUserAssociation(db.Model):
    __tablename__ = 'team_members'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'), primary_key=True)
    role = db.Column(db.String(50))
    
    user = db.relationship(User, back_populates="team_associations")
    team = db.relationship(Team, back_populates="team_associations")

class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign Keys
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('athletes.colby_id'))

    # Relationships
    creator = db.relationship('User', foreign_keys=[creator_id], backref='created_notes')
    receiver = db.relationship('Athlete', foreign_keys=[receiver_id], backref='received_notes')


