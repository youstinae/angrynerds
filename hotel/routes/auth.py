from urllib.parse import urljoin, urlparse

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_user, logout_user
from flask_security.utils import encrypt_password, verify_and_update_password
from sqlalchemy.orm import exc

from hotel.db import db
from hotel.email import notify_register_account
from hotel.forms.login import LoginForm
from hotel.forms.register import RegisterForm
from hotel.forms.contactus import ContactForm
from hotel.models import Role, User, Contact

auth = Blueprint('auth', __name__, url_prefix='/auth')



@auth.route('/contactus', methods=['GET', 'POST'])
def contactus():
    """
    Handle requests to the /contactus route
    Add an user to the database through the registration form
    """

    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        contact = Contact(name=name,
                          email=email,
                          subject=subject,
                          message=message)

        # add contact message to the database
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been sent!')

        # redirect to the login page
        return redirect(url_for('public.index'))
    else:
        flash('form is not valid: %s' % form.errors.items())
    # load contact template
    return render_template('auth/register.html', form=form, title='Register')


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
        password = encrypt_password(form.password.data)

        role_user = Role.query.filter_by(name='user').first()
        user = User(username=username,
                    password=encrypt_password(password),
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
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data, user):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('public.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


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


def verify_password(username, secret):
    """Verify a username/hashed password tuple."""

    try:
        user = User.query.filter_by(username=username).one()
    except exc.NoResultFound:
        # We found no username that matched
        return False

    # Perform password hash comparison in time-constant manner.
    verified = verify_and_update_password(secret, user)
    if verified is True:
        g.current_user = user
    return verified


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
