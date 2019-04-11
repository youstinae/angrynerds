""" seeder module """

from datetime import datetime

import requests
from flask import current_app

from hotel.db import db
from hotel.models import Comment, Post, Role, Room, Tag, User


def init_data():
    """ initialize data """
    with current_app.app_context():
        create_roles()
        create_users()
        create_posts()
        create_rooms()


def create_roles():
    """ create default roles """
    db.session.add_all([
        Role(name='admin'),
        Role(name='user')])
    db.session.commit()


def create_users():
    """ create default users """
    role_admin = Role.query.filter_by(name='admin').first()
    role_user = Role.query.filter_by(name='user').first()

    user = create_admin(username='gharzedd@mail.usf.edu',
                        password=enc_password('admin'),
                        roles=[role_admin])
    user.first_name = 'Marwan'
    user.last_name = 'Gharzeddine'
    user.address = '123 Tampa Rd'
    user.city = 'Tampa'
    user.state = 'FL'
    user.zipcode = 33625
    db.session.add(user)
    db.session.add(create_admin(username='schultz7@mail.usf.edu',
                                password=enc_password('admin'),
                                roles=[role_admin]))
    db.session.add(create_admin(username='user@test.com',
                                password=enc_password('test'),
                                roles=[role_user]))
    db.session.commit()


def create_rooms():
    """ create default rooms """
    for i in range(1, 61):
        db.session.add_all([
            Room(roomtype='Single'),
            Room(roomtype='Double'),
            Room(roomtype='Honeymoon'),
            Room(roomtype='Economy')
        ])
    db.session.commit()


def enc_password(secret):
    """ encrypt password """
    if secret:
        return secret
        # return sha.hash(secret)
    else:
        return None


def create_admin(username, password, roles):
    """ create admin user """
    return User(username=username,
                password=enc_password(password),
                email=username,
                active=True,
                confirmed=True,
                confirmed_on=datetime.utcnow(),
                registered_on=datetime.utcnow(),
                roles=roles)


def create_user(username, password, roles):
    """ create user """
    return User(username=username,
                password=enc_password(password),
                email=username,
                active=False,
                confirmed=False,
                registered_on=datetime.utcnow(),
                roles=roles)


def create_posts():
    """ create default blogs """
    username = 'gharzedd@mail.usf.edu'
    user = User.query.filter_by(username=username).first()

    content = create_blog_content('/ul/dl/bq/headers')
    post = create_post(title='Title 1',
                       summary='my summary 1',
                       content=content,
                       author_id=user.id)
    db.session.add(post)

    content = create_blog_content('/ol/bq/headers/allcaps')
    post = create_post(title='Title 2',
                       summary='my summary 2',
                       content=content,
                       author_id=user.id)
    db.session.add(post)
    db.session.commit()


def create_blog_content(options='/10/medium/link'):
    """
    creates a lorem ipsum blog texts using https://loripsum.net
    All options are turned on by default. Turn them off as needed.

    API options:
    (integer) - The number of paragraphs to generate.
    short, medium, long, verylong - The average length of a paragraph.
    decorate - Add bold, italic and marked text.
    link - Add links.
    ul - Add unordered lists.
    ol - Add numbered lists.
    dl - Add description lists.
    bq - Add blockquotes.
    code - Add code samples.
    headers - Add headers.
    allcaps - Use ALL CAPS.
    prude - Prude version.
    plaintext - Return plain text, no HTML.
    """
    api = 'https://loripsum.net/api'
    api = '{}/{}'.format(api, options)

    response = requests.get(api)
    post = response.text.replace(" ", "")
    post = response.text.replace("\n", "")
    return post


def create_post(title, summary, content, author_id):
    """ create a post entity """
    post = Post(title=title,
                summary=summary,
                content=content,
                created=datetime.utcnow(),
                published=True,
                author_id=author_id)
    return post
