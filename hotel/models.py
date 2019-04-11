""" app modules  """
from datetime import datetime

from flask_login import UserMixin

from hotel.db import db


class UsersRoles(db.Model):
    """ User model """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'role.id', ondelete='CASCADE'))


class User(db.Model, UserMixin):
    """ Create a User table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    # nullable columns
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(), nullable=True)
    state = db.Column(db.String(), nullable=True)
    zipcode = db.Column(db.String(), nullable=True)
    confirmed_on = db.Column(db.DateTime(), nullable=True)

    # relations
    posts = db.relationship('Post', backref='user', lazy=True)
    rooms = db.relationship('Room', backref='room', lazy=True)
    roles = db.relationship('Role', secondary='users_roles', lazy='subquery',
                            backref=db.backref('user', lazy=True))

    def validate(self, password):
        """ validate password """
        return password == self.password
        # return sha.verify(password, self.password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Role(db.Model):
    """ Create a Role table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.    String(), unique=True)
    description = db.Column(db.String())

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Post(db.Model):
    """ Create a blog table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    summary = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    published = db.Column(db.Boolean(), nullable=False, default=False)
    views_count = db.Column(db.Integer(), nullable=False, default=0)
    comment_count = db.Column(db.Integer(), nullable=False, default=0)
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime(), default=datetime.utcnow())
    comments = db.relationship('Comment', backref='post', lazy=True)
    tags = db.relationship('Tag', secondary='posts_tags', lazy='subquery',
                           backref=db.backref('post', lazy=True))
    author_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % (self.title)


class Comment(db.Model):
    """ Create a Comment table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    name = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    post_id = db.Column(
        db.Integer(), db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return '<Comment %r>' % (self.subject)


class PostsTags(db.Model):
    """ create a posts tags table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey(
        'post.id', ondelete='CASCADE'))
    tag_id = db.Column(db.Integer(), db.ForeignKey(
        'tag.id', ondelete='CASCADE'))


class Tag(db.Model):
    """ Create a tags table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    post_id = db.Column(
        db.Integer(), db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return '<Tag %r>' % (self.name)


class Room(db.Model):
    """ Create a Room table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    open = db.Column(db.Boolean(), unique=False, default=True)
    tenant_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=True)
    roomtype = db.Column(db.String(), nullable=False)


class Contact(db.Model):
    """ Create a Contact Message table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String())
    message = db.Column(db.String(), nullable=False)


class Feedback(db.Model):
    """ Create a Feedback Message table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String())
    message = db.Column(db.String(), nullable=False)
