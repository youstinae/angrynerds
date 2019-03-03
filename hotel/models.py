from flask_security import UserMixin, RoleMixin
from hotel import db


# roles_users = db.Table('users_roles',
#                        db.Column('user_id', db.Integer(),
#                                  db.ForeignKey('user.id')),
#                        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class UsersRoles(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    user = db.relationship('User', backref=db.backref('users', lazy='dynamic'))
    role = db.relationship('Role', backref=db.backref('roles', lazy='dynamic'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.String, nullable=True)
    roles = db.relationship(
        'UsersRoles', backref=db.backref('role', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % (self.email)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String, nullable=True)
    users = db.relationship(
        'UsersRoles', backref=db.backref('user', lazy='dynamic'))

    def __repr__(self):
        return '<Role %r>' % (self.name)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(
        'User', backref=db.backref('users', lazy='joined'))

    def __init__(self, title, author, image=None, rating=0):
        self.title = title
        self.author = author
        self.image = image
        self.rating = rating

    def __repr__(self):
        return '<Blog %r>' % (self.title)
