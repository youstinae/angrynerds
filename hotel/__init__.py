from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

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

    Bootstrap(app)

    from hotel.routes import public as public_blueprint
    from hotel.routes import auth as auth_blueprint
    from hotel.routes import admin as admin_blueprint

    app.register_blueprint(public_blueprint.public)
    app.register_blueprint(admin_blueprint.admin)
    app.register_blueprint(auth_blueprint.auth)

    return app
