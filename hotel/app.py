from werkzeug.security import generate_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask import (Flask, render_template, request, current_app)
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_mail import Mail

from hotel import auth, blog
from hotel.database import session, init_db
from hotel.models import User, Role

app = Flask(__name__)
app.config.from_object('config.Develop')

# blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
mail = Mail(app)

# database
db = SQLAlchemy(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(session, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    # drop database
    db.reflect()
    db.drop_all()

    # reinitialize db
    init_db()

    # seed data
    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='user')
    user_datastore.commit()

    user_datastore.create_user(username='gharzedd@mail.usf.edu',
                               password=generate_password_hash('admin'),
                               email='gharzedd@mail.usf.edu',
                               roles=['admin'])
    user_datastore.commit()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


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
