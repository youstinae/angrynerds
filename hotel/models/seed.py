from werkzeug.security import generate_password_hash

from hotel import db
from hotel.models import User, Role


def init_data():
    if len(get_roles()) == 0:
        create_roles()
    if len(get_users()) == 0:
        create_users()


def get_roles():
    roles = db.session.query(Role)
    db.session.close()
    return roles.all()


def create_roles():
    db.session.add_all([
        Role(name='admin'),
        Role(name='user')
    ])
    db.session.commit()
    db.session.close()


def get_users():
    users = db.session.query(User)
    db.session.close()
    return users.all()


def create_users():
    role = db.session.query(Role).filter_by(name='admin').first()
    db.session.add_all([
        User(username='gharzedd@mail.usf.edu',
             password=generate_password_hash('admin'),
             email='gharzedd@mail.usf.edu',
             roles=[role])
    ])
    db.session.commit()
    db.session.close()
