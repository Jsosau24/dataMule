from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os
from os import path

# Initialize the extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Set up the database uri
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    # Initialize the extensions with the app
    db.init_app(app)
    login_manager.init_app(app) 

    # Register blueprints
    from .auth import auth
    from .routes import routes
    from .models import User, Admin, Peak, Coach, Athlete
    app.register_blueprint(auth)
    app.register_blueprint(routes)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    if not path.exists('instance/database.db'):
        create_database(app)
    with app.app_context():
        create_dummy_users()

    return app

def create_database(app: Flask):
    #use app context in order to initialize properly
    with app.app_context():
        db.create_all()

        #debugging message
        print('Created Database')

def create_dummy_users():

    from .models import Admin, Peak, Coach, Athlete, Team, TeamUserAssociation
    
    # Admin
    user = Admin.query.first()
    if not user:
        dummy = Admin(colby_id = 0,
                    first_name = "Admin",
                    last_name = 'User',
                    password = generate_password_hash('test'),
                    email = "admin@colby.edu"
                    )
        db.session.add(dummy)
        db.session.commit()
        
    # Peak
    user = Peak.query.first()
    if not user:
        dummy = Peak(colby_id = 1,
                    first_name = "Peak",
                    last_name = 'User',
                    password = generate_password_hash('test'),
                    email = "peak@colby.edu"
                    )
        db.session.add(dummy)
        db.session.commit()
        
    # Coach
    user = Coach.query.first()
    if not user:
        dummy = Coach(colby_id = 2,
                    first_name = "Coach",
                    last_name = 'User',
                    password = generate_password_hash('test'),
                    email = "coach@colby.edu"
                    )
        db.session.add(dummy)
        db.session.commit()
        
    # Athlete
    user = Athlete.query.first()
    if not user:
        dummy = Athlete(colby_id = 3,
                    first_name = "Athlete",
                    last_name = 'User',
                    password = generate_password_hash('test'),
                    email = "athlete@colby.edu",
                    status = 0,
                    gender = 'Male',
                    class_year = 2024,
                    position = 'Pro'
                    )
        db.session.add(dummy)
        db.session.commit()

    team = Team.query.first()
    if not team:
        dummy_team = Team(
            name="Dummy Team",
        )
        db.session.add(dummy_team)
        db.session.commit()

        dummy_admin_association = TeamUserAssociation(
            user=Admin.query.first(),
            team=dummy_team,
            role='admin'
        )
        dummy_peak_association = TeamUserAssociation(
            user=Peak.query.first(),
            team=dummy_team,
            role='peak'
        )
        dummy_coach_association = TeamUserAssociation(
            user=Coach.query.first(),
            team=dummy_team,
            role='coach'
        )
        dummy_athlete_association = TeamUserAssociation(
            user=Athlete.query.first(),
            team=dummy_team,
            role='athlete'
        )

        db.session.add(dummy_admin_association)
        db.session.add(dummy_peak_association)
        db.session.add(dummy_coach_association)
        db.session.add(dummy_athlete_association)
        db.session.commit()


    
