from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import Email, EqualTo, Length, Required

from hotel.models import User


class ContactForm(FlaskForm):
    """
    Form for submiting a contact form
    """
    name = StringField(
        'Name', [Required(), Length(min=2, max=50)])

    email = PasswordField(
        'Email', [Email(), Required(), Length(min=6, max=50)])

    subject = StringField(
        'Subject', [Required(), Length(min=2, max=50)])

    message = StringField(
        'Message', [Required(), Length(min=10, max=250)])


    submit = SubmitField('SendMessage')



class RegisterForm(FlaskForm):
    """
    Form for users to create new account
    """
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

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')
