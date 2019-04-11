""" auth routes """

from datetime import datetime

from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_user, logout_user
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import exc

from hotel.db import db
from hotel.email import send_email
from hotel.forms.login import LoginForm
from hotel.forms.profile import PasswordForm, UsernameForm
from hotel.forms.register import ReconfirmForm, RegisterForm
from hotel.models import Role, User
from hotel.utils import is_safe_url

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ login route """
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
            confirm_url = url_for('auth.confirm_with_token',
                                  token=token, _external=True)
            html = render_template('mail/mail_confirm.html',
                                   confirm_url=confirm_url)
            send_email(user.email,
                       'Royal Hotel - Please confirm your email',
                       html)
        return redirect(url_for('auth.confirm'))
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/reset', methods=["GET", "POST"])
def reset():
    """ reset account route """
    form = UsernameForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first_or_404()
        if not user:
            flash('Account doesn\'t exist!', 'error')
            return render_template('auth/pass_reset.html', form=form)
        else:
            send_password_reset_email(username)
            flash('Please check your email for a password reset link.',
                  'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/pass_reset.html', form=form)


@auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    """ reset account with token """
    time_serial = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    salt = current_app.config['SECURITY_PASSWORD_SALT']
    username = time_serial.loads(token, salt=salt, max_age=86400)

    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404()
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been reset!')
        return redirect(url_for('auth.login'))
    return render_template('auth/pass_change.html', form=form, token=token)


@auth.route('/confirm/<token>')
def confirm_with_token(token):
    """ confirm account with token """
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
    """ reconfirm account with token """
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = ReconfirmForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first_or_404()
        if user and not user.confirmed:
            token = generate_confirmation_token(username)
            confirm_url = url_for('auth.confirm_with_token',
                                  token=token, _external=True)
            html = render_template('mail/mail_confirm.html',
                                   confirm_url=confirm_url)
            send_email(username, 'Royal Hotel-confirm account', html)
            return redirect(url_for('auth.confirm'))
    return render_template('auth/account_reconfirm.html', form=form)


@auth.route('/confirm')
def confirm():
    """ render confirm account template """
    return render_template('auth/account_confirm.html')


@auth.route('/confirmed')
def confirmed():
    """ render confirmed account template """
    return render_template('auth/account_confirmed.html')


@auth.route('/noconfirm')
def noconfirm():
    """ render noconfirm account template """
    return render_template('auth/account_noconfirm.html')


@auth.route('/logout')
def logout():
    """ logout user """
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('auth.login'))


def get_user():
    """ get user information """
    if g.current_user.id != id:
        # A user may only access their own user data.
        abort(403, message="You have insufficient permissions "
              "to access this resource.")
    try:
        user = User.query.filter(User.id == id).one()
    except exc.NoResultFound:
        abort(404, message="No such user exists!")
    data = dict(
        id=user.id,
        username=user.username,
        email=user.email,
        created_on=user.created_on)
    return data, 200


def send_password_reset_email(user_email):
    """ send password reset email """
    time_serial = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    salt = current_app.config['SECURITY_PASSWORD_SALT']
    password_reset_url = url_for(
        'auth.reset_with_token',
        token=time_serial.dumps(user_email, salt=salt),
        _external=True)
    html = render_template('mail/pass_reset.html',
                           password_reset_url=password_reset_url)
    send_email(user_email, 'Royal Hotel - password reset', html)


def generate_confirmation_token(email):
    """ generate email confirmation token """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email,
                            salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    """ confirm email token """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = serializer.loads(
        token,
        salt=current_app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration
    )
    return email
