from flask_security.utils import encrypt_password
from hotel import app
from hotel import db


def create_roles(ctx):
    ctx.create_role(name='admin')
    ctx.create_role(name='user')
    ctx.commit()


def create_users(ctx):
    users = [('gharzedd@mail.usf.edu', 'admin', '1234', ['admin'], True)]
    for user in users:
        email = user[0]
        username = user[0]
        password = user[1]
        is_active = user[4]

        if password is not None:
            password = encrypt_password(password)

        roles = [ctx.find_or_create_role(rn) for rn in user[3]]
        ctx.commit()

        user = ctx.create_user(
            email=email, username=username,
            password=password, active=is_active)
        ctx.commit()

        for role in roles:
            ctx.add_role_to_user(user, role)
        ctx.commit()


data_store = app.security.datastore
with app.app_context():
    db.drop_all()
    db.create_all()

    create_roles(data_store)
    create_users(data_store)
