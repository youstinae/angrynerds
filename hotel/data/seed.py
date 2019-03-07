from hotel.data.base import Session, engine, Base
from hotel.data.role import Role
from hotel.data.user import User

# generate database schema
Base.metadata.create_all(engine)

# create a new session
session = Session()


def init_data():
    # create roles
    role_admin = Role(name='admin')
    role_user = Role(name='user')

    # create users
    user_admin = User(username='gharzedd@mail.usf.edu',
                      password='letmein', email='gharzedd@mail.usf.edu')

    # add roles to users
    user_admin.roles = [role_admin]

    # add to session
    session.add(role_admin)
    session.add(role_user)
    session.add(user_admin)

    # commit and close session
    session.commit()
    session.close()
