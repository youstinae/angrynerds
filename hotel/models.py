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
    cancelled = db.Column(db.Boolean(), nullable=False, default=False)

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
    image_path = db.Column(db.String(), nullable=True)
    image_feature1 = db.Column(db.String(), nullable=True)
    image_feature2 = db.Column(db.String(), nullable=True)
    image_feature3 = db.Column(db.String(), nullable=True)
    view_count = db.Column(db.Integer(), nullable=False, default=0)
    comment_count = db.Column(db.Integer(), nullable=False, default=0)
    published = db.Column(db.Boolean(), nullable=False, default=False)
    publish_date = db.Column(db.DateTime())
    created = db.Column(db.DateTime(), nullable=False)
    updated = db.Column(db.DateTime(), default=datetime.utcnow())
    comments = db.relationship(
        'Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    tags = db.relationship('Tag',
                           secondary='posts_tags',
                           lazy='subquery',
                           backref=db.backref('post', lazy=True))
    author_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User')

    def __repr__(self):
        return '<Post %r>' % (self.title)


class Comment(db.Model):
    """ Create a Comment table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    post_id = db.Column(
        db.Integer(), db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return '<Comment %r>' % (self.name)


class PostsTags(db.Model):
    """ create a posts tags table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id'))


class Tag(db.Model):
    """ Create a tags table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return '<Tag %r>' % (self.name)


class Contact(db.Model):
    """ Create a Contact Message table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String())
    message = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False, default='CONT')

    def __repr__(self):
        return '<Contact %r>' % (self.name)


class Payment(db.Model):
    """ Create a Payment table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    cardNumber = db.Column(db.String())
    month = db.Column(db.Integer())
    year = db.Column(db.Integer())
    cvv = db.Column(db.Integer())


class Newsletter(db.Model):
    """ Create a newsletter sign up table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '<Newsletter %r>' % (self.email)


class Booking(db.Model):
    """ Create a Booking table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    arrival = db.Column(db.DateTime(), nullable=False)
    departure = db.Column(db.DateTime(), nullable=False)
    adults = db.Column(db.Integer(), nullable=False)
    children = db.Column(db.Integer(), nullable=False, default=0)
    rooms = db.relationship(
        'Room', backref='booking', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return '<Booking %r>' % (self.id)


class Room(db.Model):
    """ Create a Room table """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False, default=0)
    tenant_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=True)
    booking_id = db.Column(
        db.Integer(), db.ForeignKey('booking.id'), nullable=True)

    def __repr__(self):
        return '<Room %r>' % (self.roomtype)
