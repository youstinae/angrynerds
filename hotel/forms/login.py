
from flask_wtf import FlaskForm
from wtforms.validators import Email, Required
from wtforms import (StringField, BooleanField, PasswordField,
                     SubmitField)


class LoginForm(FlaskForm):
    """ Form for users to login """
    username = StringField('Username', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')
