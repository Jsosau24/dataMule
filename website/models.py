# imports
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# models

# User class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

    role = db.Column(db.Integer)
    notes_permissions = db.Column(db.Integer)

# Athlete Class
class Athlete(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    status = db.Column(db.Integer)

    # relationship/connection to other models
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    notes = db.relationship('Note')

# Staff/Coach Class
class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    # relationship/connection to other models
    teams = db.relationship('Team')

# Team Class
class Team(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    team_name = db.Column(db.String(150), unique=True)

   # relationship/connection to other models
    coach_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    athletes = db.relationship('Athlete')

# Note Class
class Note(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 

    writer_id = db.Column(db.Integer) 
    content = db.Column(db.String(1500)) 

    # relationship/connection to other models
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id')) 
    


