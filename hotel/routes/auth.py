from datetime import datetime

from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_user, logout_user
# from flask_security.utils import hash_password
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import exc
# from passlib.hash import pbkdf2_sha256 as sha

from hotel.db import db
from hotel.email import notify_confirm_account
from hotel.forms.login import LoginForm
from hotel.forms.register import RegisterForm, ReconfirmForm
from hotel.models import Role, User
from hotel.utils import is_safe_url

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        secret = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not user.validate(secret):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        elif not user.confirmed:
            return redirect(url_for('auth.noconfirm'))
        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('public.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        # password = sha.hash_password(form.password.data)
        password = form.password.data
        role_user = Role.query.filter_by(name='user').first()
        user = User(username=username,
                    password=password,
                    email=username,
                    active=True,
                    confirmed=False,
                    registered_on=datetime.utcnow(),
                    roles=[role_user])
        db.session.add(user)
        db.session.commit()
        if (current_app.config['MAIL_ENABLED']):
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('auth.confirm_email',
                                  token=token, _external=True)
            html = render_template('mail/mail_confirm.html',
                                   confirm_url=confirm_url)
            notify_confirm_account(user.email, html)
        return redirect(url_for('auth.confirm'))
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/confirm/<token>')
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return redirect(url_for('auth.confirm'))
    else:
        user.confirmed = True
        user.confirmed_on = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('auth.confirmed'))


@auth.route('/reconfirm', methods=['GET', 'POST'])
def reconfirm():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = ReconfirmForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first_or_404()
        if user and not user.confirmed:
            token = generate_confirmation_token(username)
            confirm_url = url_for('auth.confirm_email',
                                  token=token, _external=True)
            html = render_template('mail/mail_confirm.html',
                                   confirm_url=confirm_url)
            notify_confirm_account(username, html)
            return redirect(url_for('auth.confirm'))
    return render_template('auth/account_reconfirm.html', form=form)


@auth.route('/confirm')
def confirm():
    return render_template('auth/account_confirm.html')


@auth.route('/confirmed')
def confirmed():
    return render_template('auth/account_confirmed.html')


@auth.route('/noconfirm')
def noconfirm():
    return render_template('auth/account_noconfirm.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def get_user(user_id):
    """Handling of creating a user."""
    if g.current_user.id != user_id:
        # A user may only access their own user data.
        abort(403, message="You have insufficient permissions "
              "to access this resource.")
    try:
        user = User.query.filter(User.id == user_id).one()
    except exc.NoResultFound:
        abort(404, message="No such user exists!")

    data = dict(
        id=user.id,
        username=user.username,
        email=user.email,
        created_on=user.created_on)
    return data, 200


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email,
                            salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = serializer.loads(
        token,
        salt=current_app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration
    )
    return email
