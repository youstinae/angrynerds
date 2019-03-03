import os
from datetime import datetime

import bcrypt
from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for, current_app)
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_security.utils import hash_password

from flask_mail import Mail
from cache import cache

from hotel import auth
from hotel import blog
# from hotel.models import User, Role
from hotel.forms.account import LoginForm, RegisterForm

app = Flask(__name__)
app.config.from_object('config.Develop')

# apply the blueprints to the app
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
app.add_url_rule('/', endpoint='index')

db = SQLAlchemy(app)
cache.init_app(app)
# db.init_app(app)
mail = Mail(app)

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.String())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return '<User id=%s email=%s>' % (self.id, self.email)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all(app=app)

    user_datastore.find_or_create_role(
        name='admin', description='an admin role')
    user_datastore.find_or_create_role(name='user', description='a user role')

    if not user_datastore.get_user('gharzedd@mail.usf.edu'):
        user_datastore.create_user(email='gharzedd@mail.usf.edu',
                                   password=hash_password('letmein'),
                                   active=True,
                                   confirmed_at=datetime.utcnow())

    user_datastore.add_role_to_user('gharzedd@mail.usf.edu', 'admin')
    db.session.commit()


@cache.cached(300)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/accomodation')
def accomodation():
    return render_template('accomodation.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.errorhandler(404)
def not_found(error):
    current_app.logger.error('Page not found: %s', (request.path, error))
    return render_template('error_404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    current_app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500


@app.errorhandler(Exception)
def unhandled_exception(error):
    current_app.logger.error('Unhandled Exception: %s', (error))
    return render_template('error_500.html'), 500


if __name__ == "__main__":
    app.run()
