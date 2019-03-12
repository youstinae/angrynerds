from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy

from flask_bootstrap import Bootstrap
from hotel.config import configure_app
from hotel.models.db import db, login_manager
# from hotel.models.seed import init_database
from hotel.routes import admin as admin_blueprint
from hotel.routes import auth as auth_blueprint
from hotel.routes import blog as blog_blueprint
from hotel.routes import public as public_blueprint

app = Flask(__name__)
configure_app(app)

# db = SQLAlchemy(app=app)
# login_manager = LoginManager()
db.init_app(app)

#  init_database()

login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

Bootstrap(app)

app.register_blueprint(public_blueprint.public)
app.register_blueprint(admin_blueprint.admin)
app.register_blueprint(auth_blueprint.auth)
app.register_blueprint(blog_blueprint.blog)
