from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Email, Length, Required


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
