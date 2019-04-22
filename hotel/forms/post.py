""" module for blog posts """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Length, Required


class PostForm(FlaskForm):
    """ Form to create new blog post  """
    title = StringField('Title', [Required(), Length(min=6, max=128)])
    summary = TextAreaField('Title', [Required(), Length(min=6, max=128)])
    content = TextAreaField('Content', [Required()])
    submit = SubmitField('Create')


class PostUpdateForm(FlaskForm):
    """ blog update form """
    title = StringField('Title',
                        validators=[Required(), Length(min=1, max=128)])
    summary = TextAreaField('Summary',
                            validators=[Required(), Length(min=1, max=500)])
    content = TextAreaField('Content',
                            validators=[Required(), Length(min=1, max=10000)])
    published = BooleanField('Published', validators=[Required()])
    submit = SubmitField('Update Post')
