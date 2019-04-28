""" seeder module """

import random
from datetime import datetime
from random import randint

from flask import current_app

from hotel.db import db
from hotel.models import Comment, Post, Role, Room, Tag, User
from hotel.utils import get_random_date


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
    db.session.add(Room(type='Single', quantity=25))
    db.session.add(Room(type='Double', quantity=25))
    db.session.add(Room(type='Honeymoon', quantity=25))
    db.session.add(Room(type='Economy', quantity=25))
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
    db.session.add(Tag(name='Lifestyle'))  # 0
    db.session.add(Tag(name='Fashion'))  # 1
    db.session.add(Tag(name='Art'))  # 2
    db.session.add(Tag(name='Adventure'))  # 3
    db.session.add(Tag(name='Weddings'))  # 4
    db.session.add(Tag(name='Outdoor'))  # 5
    db.session.add(Tag(name='Social Life'))  # 6
    db.session.add(Tag(name='Business'))  # 7
    db.session.add(Tag(name='Food'))  # 8
    db.session.commit()


def create_posts():
    """ create default blogs """
    tags = Tag.query.all()
    db.session.add(
        create_post(title='Share Your Love of Travel',
                    summary=get_summary(),
                    content='coming soon',
                    published=True,
                    image_path='/static/image/blog/main-blog/m-blog-1.jpg',
                    tags=[tags[0], tags[3]]))
    db.session.add(
        create_post(title='Spring Discounts To Take Advantage Off',
                    summary=get_summary(),
                    content='coming soon',
                    published=True,
                    image_path='/static/image/blog/main-blog/m-blog-2.jpg',
                    tags=tags))
    db.session.add(
        create_post(title='7 Ingenious Tips For Hotel Wedding',
                    summary=get_summary(),
                    content='coming soon',
                    published=True,
                    image_path='/static/image/blog/main-blog/m-blog-3.jpg',
                    tags=[tags[0], tags[4]]))
    db.session.add(
        create_post(title='Top Five Trends In Outdoor To Watch',
                    summary=get_summary(),
                    content='coming soon',
                    published=True,
                    image_path='/static/image/blog/main-blog/m-blog-4.jpg',
                    tags=[tags[0], tags[3], tags[5]]))
    db.session.add(
        create_post(title='Get Social With A Custom Hashtag',
                    summary=get_summary(),
                    content='coming soon',
                    published=False,
                    image_path='/static/image/blog/main-blog/m-blog-5.jpg',
                    tags=[tags[0], tags[3], tags[5], tags[7]]))
    db.session.commit()

    for i in range(1, 31):
        db.session.add(
            create_post(title='Lorem aut saepe recusandae aut dolore',
                        summary=get_summary(),
                        content='coming soon',
                        published=True,
                        image_path='https://picsum.photos/555/280/?random={}'.format(
                            i),
                        tags=[tags[randint(0, 7)],
                              tags[randint(0, 7)]
                              ]))
        db.session.commit()


def create_post(title, summary, content, published, image_path, tags):
    """ create a post entity """
    user = User.query.filter_by(username='gharzedd@mail.usf.edu').first()
    post = Post(title=title,
                summary=summary,
                content=content,
                image_path=image_path,
                image_feature1='https://picsum.photos/750/350/?random',
                image_feature2='https://picsum.photos/360/350/?random',
                image_feature3='https://picsum.photos/g/360/350/?random',
                view_count=random.randint(1, 3001),
                tags=tags,
                created=datetime.utcnow(),
                published=published,
                publish_date=get_random_date(2018),
                author_id=user.id)

    post.comments.append(
        Comment(name='Emilly Blunt',
                email=user.username,
                content='Never say goodbye till the end comes!'))
    post.comments.append(
        Comment(name='Elsie Cunningham',
                email=user.username,
                content='Never say goodbye till the end comes!'))
    post.comments.append(
        Comment(name='Annie Stephens',
                email=user.username,
                content='Never say goodbye till the end comes!'))
    post.comments.append(
        Comment(name='Maria Luna',
                email=user.username,
                content='Never say goodbye till the end comes!'))
    post.comments.append(
        Comment(name='Ina Hayes',
                email=user.username,
                content='Never say goodbye till the end comes!'))
    post.comment_count = 5
    return post


def get_summary():
    return ('MCSE boot camps have its supporters and its detractors. '
            'Some people do not understand why you should have to spend '
            'money on boot camp when you can get the MCSE study materials '
            'yourself at a fraction.')
