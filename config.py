""" configuration module """

import logging
import os

from hotel.utils import get_app_base_path


class Base():
    """ base configuration """
    DEBUG = False
    CSRF_ENABLED = True

    # DIRECTORIES
    APP_DIR = get_app_base_path()
    STATIC_DIR = os.path.join(APP_DIR, 'hotel/static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'image')

    # DATABASE sqlite :memory: is default
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'angry5nerds'
    SECRET_KEY = 'e4923b4f-b7f3-4127-aaeb-06b4e341a9f7'
    SESSION_PERMANENT = False

    # MAIL
    MAIL_DEFAULT_SENDER = 'royal.hotel@localhost.local'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_ENABLED = True

    # PAGING
    POSTS_PER_PAGE = 5

    # editor
    CKEDITOR_PKG_TYPE = 'basic'


class Development(Base):
    """ development configuration """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/hotel.db'
    SECRET_KEY = '2da1d68d-e48a-45aa-8a37-b2b9ce1ee91b'
