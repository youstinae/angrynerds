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

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .public import public as public_blueprint
    app.register_blueprint(public_blueprint)

    @app.route('/')
    def home():
        return 'Welcome, Home!'

    return app
