from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, HiddenField, TextField, SubmitField, validators


class RegisterForm(FlaskForm):
    username = StringField('Username', [
        validators.Email('Email Address'),
        validators.Length(min=6, max=50)
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=6, max=50)
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=5, max=15)
    ])
    remember = BooleanField('Remember me')


class SignupForm(FlaskForm):

    next = HiddenField()

    username = StringField('Email Address', [
        validators.DataRequired(),
        validators.Length(min=6, max=35)
    ])

    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    password = PasswordField('Password again', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords don\'t match')
    ])

    email = StringField('Email Address', [
        validators.DataRequired(),
        validators.email('A valid email address is required.')
    ])

    submit = SubmitField('Register')
