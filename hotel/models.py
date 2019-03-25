from flask_login import UserMixin
# from flask_security.utils import verify_and_update_password
# from passlib.hash import pbkdf2_sha256 as sha

from hotel.db import db


class UserRoles(db.Model):
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
    confirmed_on = db.Column(db.DateTime(), nullable=True)

    # relations
    posts = db.relationship('Post', backref='user', lazy=True)
    rooms = db.relationship('Room', backref='room', lazy=True)
    roles = db.relationship('Role', secondary='user_roles', lazy='subquery',
                            backref=db.backref('user', lazy=True))

    # def is_authenticated(self):
    #     return self.authenticated

    # def get_id(self):
    #     return self.id

    # def is_active(self):
    #     return True

    # def is_anonymous(self):
    #     return False

    def validate(self, password):
        return password == self.password
        # return sha.verify(password, self.password)

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


class Contact(db.Model):
    """
    Create a Contact Message table
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String())
    message = db.Column(db.String(), nullable=False)
