from datetime import datetime
from flask import current_app
# from flask_security.utils import hash_password
# from passlib.hash import pbkdf2_sha256 as sha

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
    role_admin = Role.query.filter_by(name='admin').first()
    role_user = Role.query.filter_by(name='user').first()

    db.session.add(create_admin(username='gharzedd@mail.usf.edu',
                                password=enc_password('admin'),
                                roles=[role_admin]))
    db.session.add(create_admin(username='schultz7@mail.usf.edu',
                                password=enc_password('admin'),
                                roles=[role_admin]))
    db.session.add(create_admin(username='user@test.com',
                                password=enc_password('test'),
                                roles=[role_user]))
    db.session.commit()


def enc_password(secret):
    if(secret):
        return secret
        # return sha.hash(secret)
    else:
        return None


def create_admin(username, password, roles):
    return User(username=username,
                password=enc_password(password),
                email=username,
                active=True,
                confirmed=True,
                confirmed_on=datetime.utcnow(),
                registered_on=datetime.utcnow(),
                roles=roles)


def create_user(username, password, roles):
    return User(username=username,
                password=enc_password(password),
                email=username,
                active=False,
                confirmed=False,
                registered_on=datetime.utcnow(),
                roles=roles)


# def create_posts():
#     post = Post(title='', body='')
#     db.session.add(post)

#     post = Post(title='', body='')
#     db.session.add(post)

#     db.session.commit()
