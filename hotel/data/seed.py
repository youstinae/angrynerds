from hotel.data.base import Session, engine, Base
from hotel.data.role import Role
from hotel.data.user import User
from hotel.data.post import Post

# generate database schema
Base.metadata.create_all(engine)

# create a new session
session = Session()


def init_data():
    # create roles
    role_admin = Role(name='admin')
    role_user = Role(name='user')

    # create users
    user_marwan = User(username='gharzedd@mail.usf.edu',
                       password='letmein', email='gharzedd@mail.usf.edu')

    user_jean = User(username='jean@mail.usf.edu',
                     password='password', email='jean@mail.usf.edu')

    # add roles to users
    user_marwan.roles = [role_admin]
    user_jean.roles = [role_admin]

    # add to session
    session.add(role_admin)
    session.add(role_user)
    session.add(user_marwan)
    session.add(user_jean)

    # commit and close session
    session.commit()
    session.close()


def init_posts():
    post = Post(title='first post', body='first post')
    session.add(post)
    session.commit()
    session.close()
