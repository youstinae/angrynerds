from werkzeug.security import check_password_hash, generate_password_hash

from hotel.db import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model):
    """
    Create a User table
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), index=True)
    last_name = db.Column(db.String(), index=True)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer())
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='users', lazy=True)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

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
    users = db.relationship('User', backref='user', lazy='dynamic')

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
    user = db.relationship('User')

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