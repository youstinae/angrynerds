from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Develop')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    @app.route('/')
    def home():
        return 'Welcome, Home!'

    return app
