""" Blog Update module """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import BooleanField
from wtforms.validators import Length, Required

from hotel.models import Post


class BlogUpdateForm(FlaskForm):
    """ blog update form """
    title = StringField('Title',
                        validators=[Required(), Length(min=1, max=128)])
    summary = StringField('Summary',
                          validators=[Required(), Length(min=1, max=500)])
    content = StringField('Content',
                          validators=[Required(), Length(min=1, max=10000)])
    published = BooleanField('Published', validators=[Required()])
    deleted = BooleanField('Deleted', validators=[Required()])

    submit = SubmitField('Update Post')
