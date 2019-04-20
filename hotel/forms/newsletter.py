""" newsletter form """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, Length, Required


class NewsletterForm(FlaskForm):
    """
    Form for newsletter signup
    """
    email = StringField(
        'Email', [Email(), Required(), Length(min=6, max=100)])
