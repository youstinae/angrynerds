import os
import logging

from hotel.utils import get_app_base_path


class Base():
    DEBUG = False
    CSRF_ENABLED = True

    # DIRECTORIES
    APP_DIR = get_app_base_path()
    STATIC_DIR = os.path.join(APP_DIR, 'hotel/static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'image')

    # DATABASE sqlite :memory: is default
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'angry813nerds'
    SECRET_KEY = 'e4923b4f-b7f3-4127-aaeb-06b4e341a9f7'

    # MAIL
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25

    # LOGGING
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'hotel.log'
    LOGGING_LEVEL = logging.DEBUG


class Development(Base):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/hotel.db'
    SECRET_KEY = '2da1d68d-e48a-45aa-8a37-b2b9ce1ee91b'
