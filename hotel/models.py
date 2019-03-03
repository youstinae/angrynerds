from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey

db = SQLAlchemy()


class Role(db.Model, RoleMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % (self.name)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    last_login_at = Column(DateTime)
    current_login_at = Column(DateTime)
    last_login_ip = Column(String)
    current_login_ip = Column(String)
    login_count = Column(Integer)
    active = Column(Boolean)
    confirmed_at = Column(DateTime)
    roles = db.relationship(
        'RoleUsers', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, active, roles):
        self.email = email
        self.password = password
        self.active = active
        self.roles = roles

    def __repr__(self):
        return '<User %r>' % (self.email)


class RolesUsers(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    role_id = Column('role_id', Integer, ForeignKey('role.id'))


class Blog(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    image = Column(String)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = db.relationship(
        'User', backref=db.backref('users', lazy='joined'))

    def __init__(self, title, author, image=None, rating=0):
        self.title = title
        self.author = author
        self.image = image
        self.rating = rating

    def __repr__(self):
        return '<Blog %r>' % (self.title)
