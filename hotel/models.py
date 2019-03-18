from datetime import datetime

from flask_login import UserMixin
from flask_security.utils import encrypt_password, verify_and_update_password

from hotel.db import db


class UserRoles(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'role.id', ondelete='CASCADE'))


class User(db.Model, UserMixin):
    """
    Create a User table
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), index=True)
    last_name = db.Column(db.String(), index=True)
    email = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime(), default=datetime.utcnow())
    login_count = db.Column(db.Integer())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    posts = db.relationship('Post', backref='user', lazy=True)
    rooms = db.relationship('Room', backref='room', lazy=True)
    roles = db.relationship('Role', secondary='user_roles', lazy='subquery',
                            backref=db.backref('user', lazy=True))

    # @property
    # def password(self):
    #     """ Prevent pasword from being accessed """
    #     raise AttributeError('password is not a readable attribute.')

    def set_password(self, secret):
        """ Set password to a hashed password """
        self.password = encrypt_password(secret)

    def check_password(self, secret, user):
        """ Check if hashed password matches actual password """
        result = verify_and_update_password(secret, user)
        return result

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Role(db.Model):
    """
    Create a Role table
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Post(db.Model):
    """
    Create a Post table
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    image = db.Column(db.String())
    created_on = db.Column(db.DateTime())
    updated_on = db.Column(db.DateTime())
    published_on = db.Column(db.DateTime())
    author_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % (self.title)


class Room(db.Model):
    """
    Create a Room table
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    open = db.Column(db.Boolean(), unique=False, default=True)
    tenant_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
