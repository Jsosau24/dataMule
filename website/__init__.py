# import statements
from venv import create
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
DB_NAME = "database.db"

# creates the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    db.init_app(app)

    #creates the databases
    from .models import User

    create_database(app)
    dummy_populate(app)

    # register blueprints for other pages (views and authentication)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    # stuff for login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # end of init
    return app


#function that creates the database
def create_database(app: Flask):
    ''' Creates the databse if the file doesn't exist '''
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')


#function to populate database with dummy values
def dummy_populate(app):
    with app.app_context():
        #check if there are users
        from .models import User
        check = User.query.filter_by(colby_id=0).first()
        if not check:
            #create dummy users
            jonna = User(
                colby_id = 0,
                first_name = 'Jonna',
                last_name = 'Sosa',
                password = generate_password_hash('dataMULE',method='sha256'),
                email = 'jsosau24@colby.edu',
                role = 0,
                notes_permissions = 0
            )

            # commit dummy users to the database
            db.session.add_all([jonna])
            db.session.commit()


#function to empty the database
def drop_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
    print('Database has been dropped!')

