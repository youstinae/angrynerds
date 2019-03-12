import os
import logging

from hotel.utils import get_app_base_path


class Base():
    DEBUG = False
    TESTING = False

    # DIRECTORIES
    APP_DIR = get_app_base_path()
    STATIC_DIR = os.path.join(APP_DIR, 'static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

    # DATABASE sqlite :memory: identifier is the default
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'angry813nerds'
    SECRET_KEY = 'e4923b4f-b7f3-4127-aaeb-06b4e341a9f7'

    # MAIL
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'

    # LOGGING
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'hotel.log'
    LOGGING_LEVEL = logging.DEBUG


class Development(Base):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/hotel.db'
    SECRET_KEY = '2da1d68d-e48a-45aa-8a37-b2b9ce1ee91b'


config = {
    "dev": "hotel.config.Development",
    "staging": "hotel.config.Staging",
    "prod": "hotel.config.Production",
    "default": "hotel.config.Development"
}


def configure_app(app):
    app.config.from_object(config['dev'])

    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
