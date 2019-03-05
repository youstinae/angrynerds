from datetime import datetime

from flask import (Flask, render_template, request, current_app)
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from flask_mail import Mail

from .database import db_session, init_db
from .models import User, Role
from hotel import auth
from hotel import blog

app = Flask(__name__)
app.config.from_object('config.Develop')

# apply the blueprints to the app
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
mail = Mail(app)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Create data to test with
@app.before_first_request
def seed_data():
    init_db()
    user_datastore.find_or_create_role(
        name='admin', description='an admin role')
    user_datastore.find_or_create_role(name='user', description='a user role')

    if not user_datastore.get_user('gharzedd@mail.usf.edu'):
        user_datastore.create_user(email='gharzedd@mail.usf.edu',
                                   password=hash_password('letmein'),
                                   active=True,
                                   confirmed_at=datetime.utcnow())

    user_datastore.add_role_to_user('gharzedd@mail.usf.edu', 'admin')
    db_session.commit()


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


# @app.errorhandler(500)
# def internal_server_error(error):
#     current_app.logger.error('Server Error: %s', (error))
#     return render_template('500.html'), 500


# @app.errorhandler(Exception)
# def unhandled_exception(error):
#     current_app.logger.error('Unhandled Exception: %s', (error))
#     return render_template('error_500.html'), 500


if __name__ == "__main__":
    app.run()
