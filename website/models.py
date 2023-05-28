from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    colby_id = db.Column(db.Integer)
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

team_coaches = db.Table('team_coaches',
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('coach_id', db.Integer, db.ForeignKey('coaches.colby_id'), primary_key=True)
)

team_members = db.Table('team_members',
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('athlete_id', db.Integer, db.ForeignKey('athletes.colby_id'), primary_key=True)
)

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    coach_ids = db.relationship('Coach', secondary=team_coaches, backref='teams')
    athletes = db.relationship('Athlete', secondary=team_members, lazy='subquery', backref=db.backref('teams', lazy=True))



