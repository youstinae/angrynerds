from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from hotel import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String())
    current_login_ip = db.Column(db.String())
    login_count = db.Column(db.Integer())
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

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


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
