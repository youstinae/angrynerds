from urllib.parse import urlparse, urljoin
from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   url_for, request)
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.orm import exc
from werkzeug.security import check_password_hash, generate_password_hash

from hotel.db import db
from hotel.email import notify_register_account
from hotel.forms.login import LoginForm
from hotel.forms.register import RegisterForm
from hotel.models import User
from hotel.models import Role

auth = Blueprint('auth', __name__, url_prefix='/auth')


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
        password = generate_password_hash(form.password.data)

        role_user = Role.query.filter_by(name='user').first()
        user = User(username=username,
                    password=generate_password_hash(password),
                    email=username,
                    roles=[role_user])

        # add user to the database
        db.session.add(user)
        db.session.commit()
        notify_register_account()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('public.index'))
    else:
        flash('form is not valid: %s' % form.errors.items())

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Logged in successfully.')

        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('public.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
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


def create_user(user):
    """Create a new user."""
    user = User(**user)
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        abort(409, message="User already exists!")

    data = dict(id=user.id, username=user.username,
                email=user.email, created_on=user.created_on)

    return data, 201


def verify_password(username, password):
    """Verify a username/hashed password tuple."""

    try:
        user = User.query.filter_by(username=username).one()
    except exc.NoResultFound:
        # We found no username that matched
        return False

    # Perform password hash comparison in time-constant manner.
    verified = check_password_hash(user.password, password)
    if verified is True:
        g.current_user = user
    return verified


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
