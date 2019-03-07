from flask_wtf import FlaskForm
from wtforms import (TextField, BooleanField, PasswordField, DateField)
from wtforms.validators import Email, Required, EqualTo, Length


class RegisterForm(FlaskForm):
    username = TextField(
        'Username', [Email(), Required(), Length(min=6, max=50)])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])


class LoginForm(FlaskForm):
    username = TextField('Username', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    remember = BooleanField('Remember me')
