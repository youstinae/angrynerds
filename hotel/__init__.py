import os

from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for, current_app)
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail
from cache import cache

from hotel.forms.account import LoginForm, RegisterForm
from hotel.models import db, User, Role
from hotel.auth import auth
from hotel.blog import blog


app = Flask(__name__)
app.config.from_object('config.Develop')

# apply the blueprints to the app
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
app.add_url_rule('/', endpoint='index')

cache.init_app(app)
db.init_app(app)
mail = Mail(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


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
    return render_template('500.htm'), 500


@app.errorhandler(Exception)
def unhandled_exception(error):
    current_app.logger.error('Unhandled Exception: %s', (error))
    return render_template('error_500.htm'), 500


# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='admin@mail.usf.edu', password='letmein')
    db.session.commit()


if __name__ == "__main__":
    app.run()
