from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Email, Length, Required

from hotel.models import User


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Email()])
    first_name = StringField('First Name', validators=[])
    last_name = StringField('Last Name', validators=[])

    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    """ Form for password reset """
    username = StringField(
        'Username', [Email(), Required(), Length(min=6, max=50)])

    submit = SubmitField('Submit')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError("Account does not exist!")
