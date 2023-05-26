from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Set up the database uri
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    # Initialize the extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from .auth import auth
    from .routes import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
