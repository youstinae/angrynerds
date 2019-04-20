""" newsletter form """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, Length, Required


class NewsletterForm(FlaskForm):
    """ Form for newsletter signup """
    first_name = StringField(
        'First Name', validators=[Required(), Length(min=2, max=100)])
    last_name = StringField(
        'Last Name', validators=[Required(), Length(min=2, max=200)])
    email = StringField(
        'Email', [Email(), Required(), Length(min=6, max=100)])
    submit = SubmitField('Signup')
