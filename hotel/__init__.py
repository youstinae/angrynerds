from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail

from hotel.db import db
from hotel.db import login_manager
from hotel.routes import admin as admin_blueprint
from hotel.routes import auth as auth_blueprint
from hotel.routes import blog as blog_blueprint
from hotel.routes import public as public_blueprint


app = Flask(__name__)
app.config.from_object('config.Development')
mail = Mail(app)
db.init_app(app)


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
