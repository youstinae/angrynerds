from flask_wtf import FlaskForm
from wtforms.validators import Email, Required
from wtforms import (StringField, SubmitField, TextAreaField)


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
