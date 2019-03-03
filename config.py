import os


class Base():
    DEBUG = False
    TESTING = False
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    STATIC_DIR = os.path.join(APPLICATION_DIR, 'hotel/static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'hotel/static/images')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/data/hotel.db' % APPLICATION_DIR
    SECRET_KEY = b'\x01>\x18\xc4^\xd8X\x1dT{\x1f\x16*\xf4\xba\xbd|W\x0e\x83\xb6\x8e\xc3\x13'
    SECURITY_PASSWORD_SALT = 'angry813nerds'
    CACHE_TYPE = 'simple'
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml',
                          'application/json', 'application/javascript']


class Develop(Base):
    DEBUG = True
    TESTING = True


class Testing(Base):
    DEBUG = False
    TESTING = True
