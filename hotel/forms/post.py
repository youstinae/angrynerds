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
    image_feature1 = StringField('Featured Image Path',
                                 validators=[Length(min=1, max=512)])
    image_feature2 = StringField('Post Image 1 Path',
                                 validators=[Length(min=1, max=512)])
    image_feature3 = StringField('Post Image 2 Path',
                                 validators=[Length(min=1, max=512)])
    summary = TextAreaField('Summary',
                            validators=[Required(), Length(min=1, max=500)])
    content = TextAreaField('Content',
                            validators=[Required(), Length(min=1, max=10000)])
    published = BooleanField('Published', validators=[Required()])
    submit = SubmitField('Update Post')
