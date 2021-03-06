from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import Email, EqualTo, Length, Required

from hotel.models import User


class RegisterForm(FlaskForm):
    """ Form for users to create new account """
    username = StringField(
        'Username', [Email(), Required(), Length(min=6, max=50)])

    password = PasswordField(
        'Password', [Required(), EqualTo('confirm')])

    confirm = PasswordField('Repeat Password', [
        Required(), EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class ReconfirmForm(FlaskForm):
    """ Form for users to resend actination code """
    username = StringField(
        'Username', [Email(), Required(), Length(min=6, max=50)])

    submit = SubmitField('Resend')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError("Account does not exist!")
