from flask_wtf import FlaskForm
from wtforms.validators import Email, Required
from wtforms import (StringField, SubmitField)


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Email()])
    first_name = StringField('First Name', validators=[])
    last_name = StringField('Last Name', validators=[])

    submit = SubmitField('Submit')
