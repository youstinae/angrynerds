import datetime

from flask import request
from flask_login import UserMixin, login_manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import schema


def get_user(username):
    pass


def save_user(username, password):
    pass


def get_users():
    pass


def add_user(username, password, admin):
    users.insert().values(
        username=username,
        password=password,
        email_address=username
    )


def hash_password(pw):
    hashed_pw = generate_password_hash(pw)
    return hashed_pw.decode('utf-8')


def check_password(expected_hash, pw):
    if expected_hash is not None:
        return check_password_hash(expected_hash, pw)
    return False


def set_password(password):
    pass


def check_password2(password):
    pass
