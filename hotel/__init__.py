from flask import Flask
from flask_bootstrap import Bootstrap

from hotel.db import db, login_manager
from hotel import config
from hotel.routes import admin as admin_blueprint
from hotel.routes import auth as auth_blueprint
from hotel.routes import blog as blog_blueprint
from hotel.routes import public as public_blueprint


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'e4923b4f-b7f3-4127-aaeb-06b4e341a9f7'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///hotel.db'

db.init_app(app)
app.config.from_object(config.Development)


@app.before_first_request
def init():
    from hotel import models
    db.drop_all()
    db.create_all()


login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

Bootstrap(app)

app.register_blueprint(public_blueprint.public)
app.register_blueprint(admin_blueprint.admin)
app.register_blueprint(auth_blueprint.auth)
app.register_blueprint(blog_blueprint.blog)
