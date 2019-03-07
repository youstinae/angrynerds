from flask_sqlalchemy import SQLAlchemy
from flask import (Flask, render_template, request, current_app)
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail

from hotel import auth
from hotel import blog
from hotel.data.user import User
from hotel.data.role import Role
from hotel.data.seed import init_data

app = Flask(__name__)
app.config.from_object('config.Develop')

# blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
mail = Mail(app)

# database
db = SQLAlchemy(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def initialize_database():
    """ Create all tables """
    db.create_all()
    init_data()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


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
