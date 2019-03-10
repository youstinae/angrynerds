import os


class Base():
    DEBUG = False
    TESTING = False

    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    STATIC_DIR = os.path.join(APPLICATION_DIR, 'hotel/static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

    SECRET_KEY = b'\x01>\x18\xc4^\xd8X\x1dT{\x1f\x16*\xf4\xba\xbd|W\x0e\x83\xb6\x8e\xc3\x13'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/db/hotel.db' % APPLICATION_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'angry813nerds'

    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'


class Develop(Base):
    DEBUG = True
    TESTING = True


class Testing(Base):
    DEBUG = False
    TESTING = True


app_config = {
    'dev': Develop,
    'prod': Testing
}
