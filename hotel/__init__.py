from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_wtf import CsrfProtect

from hotel.db import db
from hotel.db import login_manager
from hotel.seed import init_data
from hotel.email import mail
from hotel.models import User, Role
from hotel.routes import admin as admin_blueprint
from hotel.routes import auth as auth_blueprint
from hotel.routes import blog as blog_blueprint
from hotel.routes import public as public_blueprint
from hotel.routes import error as error_blueprint

app = Flask(__name__)
app.config.from_object('config.Development')
db.init_app(app)
mail.init_app(app)
csrf = CsrfProtect(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def init():
    from hotel import models
    db.drop_all()
    db.create_all()
    init_data()


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user


@app.context_processor
def inject_user():
    return dict(user=current_user)


login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "info"
login_manager.login_view = "auth.login"

# Bootstrap(app)

app.register_blueprint(public_blueprint.public)
app.register_blueprint(admin_blueprint.admin)
app.register_blueprint(auth_blueprint.auth)
app.register_blueprint(blog_blueprint.blog)
app.register_blueprint(error_blueprint.error)
