from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, Length, Required


class FeedbackForm(FlaskForm):
    """
    Form for submiting a feedback form
    """
    name = StringField(
        'Name', [Required(), Length(min=2, max=50)])

    email = StringField(
        'Email', [Email(), Required(), Length(min=6, max=100)])

    subject = StringField(
        'Subject', [Required(), Length(min=2, max=200)])

    message = StringField(
        'Message', [Required(), Length(min=10, max=500)])

    submit = SubmitField('Send Message')
