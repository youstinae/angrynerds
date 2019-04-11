""" module for blog posts """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Required


class PostForm(FlaskForm):
    """ Form to create new blog post  """
    title = StringField('Title', [Required(), Length(min=6, max=128)])
    body = StringField('Body', [Required()])
    submit = SubmitField('Create')
