from flask import current_app
from werkzeug.security import generate_password_hash

from hotel.db import db
from hotel.models import User
from hotel.models import Role


def init_data():
    with current_app.app_context():
        create_roles()
        create_users()


def create_roles():
    db.session.add_all([
        Role(name='admin'),
        Role(name='user')
    ])
    db.session.commit()


def create_users():
    admin = Role.query.filter_by(name='admin').first()
    user = User(username='gharzedd@mail.usf.edu',
                password=generate_password_hash('admin'),
                email='gharzedd@mail.usf.edu',
                roles=[admin])
    db.session.add(user)
    db.session.commit()
