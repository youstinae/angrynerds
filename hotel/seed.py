from datetime import datetime
from flask import current_app
from flask_security.utils import encrypt_password

from hotel.db import db
from hotel.models import User
from hotel.models import Role
# from hotel.models import Post


def init_data():
    with current_app.app_context():
        create_roles()
        create_users()
        # create_posts()


def create_roles():
    db.session.add_all([
        Role(name='admin'),
        Role(name='user')
    ])
    db.session.commit()


def create_users():
    admin = Role.query.filter_by(name='admin').first()
    db.session.add(create_user(username='gharzedd@mail.usf.edu',
                               password=encrypt_password('admin'),
                               roles=[admin]))
    db.session.add(create_user(username='schultz7@mail.usf.edu',
                               password=encrypt_password('admin'),
                               roles=[admin]))
    db.session.commit()


def create_user(username, password, roles):
    return User(username=username,
                password=encrypt_password(password),
                email=username,
                active=True,
                confirmed=True,
                confirmed_on=datetime.utcnow(),
                registered_on=datetime.utcnow(),
                roles=roles)


# def create_posts():
#     post = Post(title='', body='')
#     db.session.add(post)

#     post = Post(title='', body='')
#     db.session.add(post)

#     db.session.commit()
