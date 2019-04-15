""" comment form"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Length, Required


class CommentForm(FlaskForm):
    """ Form for submiting a comment """
    name = StringField(
        'Name', validators=[Required(), Length(min=2, max=50)])
    email = EmailField(
        'Email', validators=[Required(), Length(min=1, max=100)])
    message = StringField(
        'Message', validators=[Required(), Length(min=1, max=500)])
    submit = SubmitField('Post Comment')
