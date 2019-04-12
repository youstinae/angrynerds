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
        create_tags()
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
    user.last_name = 'G.'
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


def create_tags():
    """ create default tags """
    db.session.add(Tag(name='Food'))
    db.session.add(Tag(name='Technology'))
    db.session.add(Tag(name='Lifestyle'))
    db.session.add(Tag(name='Politics'))
    db.session.commit()


def create_posts():
    """ create default blogs """
    username = 'gharzedd@mail.usf.edu'
    user = User.query.filter_by(username=username).first()

    tags = Tag.query.all()

    db.session.add(
        create_post(title='Astronomy Binoculars A Great Alternative',
                    summary=('MCSE boot camps have its supporters and its detractors. '
                             'Some people do not understand why you should have to spend '
                             'money on boot camp when you can get the MCSE study materials '
                             'yourself at a fraction.'),
                    content='coming soon',
                    image_path='../static/image/blog/main-blog/m-blog-1.jpg',
                    view_count=128,
                    tags=tags,
                    author_id=user.id))
    db.session.add(
        create_post(title='The Basics Of Buying A Telescope',
                    summary=('MCSE boot camps have its supporters and its detractors. '
                             'Some people do not understand why you should have to spend '
                             'money on boot camp when you can get the MCSE study materials '
                             'yourself at a fraction.'),
                    content='coming soon',
                    image_path='../static/image/blog/main-blog/m-blog-2.jpg',
                    view_count=76,
                    tags=tags,
                    author_id=user.id))
    db.session.add(
        create_post(title='The Basics Of Buying A Telescope',
                    summary=('MCSE boot camps have its supporters and its detractors. '
                             'Some people do not understand why you should have to spend '
                             'money on boot camp when you can get the MCSE study materials '
                             'yourself at a fraction.'),
                    content='coming soon',
                    image_path='../static/image/blog/main-blog/m-blog-3.jpg',
                    view_count=2100,
                    tags=tags,
                    author_id=user.id))
    db.session.add(
        create_post(title='The Night Sky',
                    summary=('MCSE boot camps have its supporters and its detractors. '
                             'Some people do not understand why you should have to spend '
                             'money on boot camp when you can get the MCSE study materials '
                             'yourself at a fraction.'),
                    content='coming soon',
                    image_path='../static/image/blog/main-blog/m-blog-4.jpg',
                    view_count=114,
                    tags=tags,
                    author_id=user.id))
    db.session.add(
        create_post(title='Telescopes 101',
                    summary=('MCSE boot camps have its supporters and its detractors. '
                             'Some people do not understand why you should have to spend '
                             'money on boot camp when you can get the MCSE study materials '
                             'yourself at a fraction.'),
                    content='coming soon',
                    image_path='../static/image/blog/main-blog/m-blog-5.jpg',
                    view_count=374,
                    tags=tags,
                    author_id=user.id))
    db.session.commit()


def create_post(title, summary, content, image_path, tags, view_count, author_id):
    """ create a post entity """
    post = Post(title=title,
                summary=summary,
                content=content,
                image_path=image_path,
                view_count=view_count,
                tags=tags,
                created=datetime.utcnow(),
                published=True,
                author_id=author_id)
    return post
