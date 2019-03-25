from datetime import datetime

from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
# from flask_security.utils import hash_password
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import exc
# from passlib.hash import pbkdf2_sha256 as sha

from hotel.db import db
from hotel.email import notify_confirm_account
from hotel.forms.login import LoginForm
from hotel.forms.register import RegisterForm
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
                    active=False,
                    confirmed=False,
                    registered_on=datetime.utcnow(),
                    roles=[role_user])
        db.session.add(user)
        db.session.commit()
        if (current_app.config['MAIL_ENABLED']):
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('auth.confirm_email',
                                  token=token, _external=True)
            html = render_template('email/email_confirm.html',
                                   confirm_url=confirm_url)
            notify_confirm_account(user.email, html)
        flash('You have successfully registered! You may now login.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('emails/unconfirmed.html')


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
