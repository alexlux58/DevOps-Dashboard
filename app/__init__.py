from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Initialize the SQLAlchemy object to interact with the database
db = SQLAlchemy()

# Set the name of the users' database file
DB_NAME_USERS = "database.db"

# Set the name of the services' database file (currently commented out)
# DB_NAME_SERVICES = "services_database.db"


def create_app():
    # Create the Flask application instance
    app = Flask(__name__)

    # Set the secret key for the application (required for sessions)
    app.config["SECRET_KEY"] = "SECRET"

    # Enable debug mode for development (disabled in production)
    app.config["DEBUG"] = True

    # Set the URI for the users' database using SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME_USERS}"

    # Bind the services database to a different name (currently commented out)
    # app.config["SQLALCHEMY_BINDS"] = {
    #     "services": f"sqlite:///{DB_NAME_SERVICES}"
    # }

    # Initialize the SQLAlchemy database with the Flask app
    db.init_app(app)

    # Import the 'views' and 'auth' blueprints for routing
    from app.views import views
    from app.auth import auth

    # Register the 'views' and 'auth' blueprints with appropriate prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import the 'User' model to interact with the user table
    from app.models import User

    # Create all the database tables defined in models.py
    create_database(app)

    # Initialize the Flask-Login extension to manage user sessions
    login_manager = LoginManager(app)

    # Set the login view for unauthorized access redirects
    login_manager.login_view = 'auth.login'

    # Initialize the login manager with the Flask app
    login_manager.init_app(app)

    # Function to load the user object from the database based on user ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Custom template global function 'my_int' to convert values to integers
    @app.template_global()
    def my_int(val):
        return int(val)

    return app


def create_database(app):
    # Check if the users' database file does not exist
    if not path.exists('./' + DB_NAME_USERS):
        # Create all database tables within the app's context
        with app.app_context():
            db.create_all()
            print('Created Database!')
