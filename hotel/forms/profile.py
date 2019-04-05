from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, StringField, SubmitField,
                     ValidationError)
from wtforms.fields.core import SelectField
from wtforms.validators import Email, Length, Required

from hotel.models import User


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    email = StringField('Email Address', validators=[Required(), Email()])
    address = StringField('Address', validators=[Required()])
    city = StringField('City', validators=[Required()])
    state = SelectField("State",
                        validators=[Required()],
                        choices=[
                            ("AK", "Alaskal"),
                            ("AL", "Alabama"),
                            ("AR", "Arkansas"),
                            ("AZ", "Arizona"),
                            ("CA", "California"),
                            ("CO", "Colorado"),
                            ("CT", "Connecticut"),
                            ("DC", "District of Columbia"),
                            ("DE", "Delaware"),
                            ("FL", "Florida"),
                            ("GA", "Georgia"),
                            ("HI", "Hawaii"),
                            ("IA", "Iowa"),
                            ("ID", "Idaho"),
                            ("IL", "Illinois"),
                            ("IN", "Indiana"),
                            ("KS", "Kansas"),
                            ("KY", "Kentucky"),
                            ("LA", "Louisiana"),
                            ("MA", "Massachusetts"),
                            ("MD", "Maryland"),
                            ("ME", "Maine"),
                            ("MI", "Michigan"),
                            ("MN", "Minnesota"),
                            ("MO", "Missouri"),
                            ("MS", "Mississippi"),
                            ("MT", "Montana"),
                            ("NC", "North Carolina"),
                            ("ND", "North Dakota"),
                            ("NE", "Nebraska"),
                            ("NH", "New Hampshire"),
                            ("NJ", "New Jersey"),
                            ("NM", "New Mexico"),
                            ("NV", "Nevada"),
                            ("NY", "New York"),
                            ("OH", "Ohio"),
                            ("OK", "Oklahoma"),
                            ("OR", "Oregon"),
                            ("PA", "Pennsylvania"),
                            ("PR", "Puerto Rico"),
                            ("RI", "Rhode Island"),
                            ("SC", "South Carolina"),
                            ("SD", "South Dakota"),
                            ("TN", "Tennessee"),
                            ("TX", "Texas"),
                            ("UT", "Utah"),
                            ("VA", "Virginia"),
                            ("VT", "Vermont"),
                            ("WA", "Washington"),
                            ("WI", "Wisconsin"),
                            ("WV", "West Virginia"),
                            ("WY", "Wyoming")])
    zipcode = IntegerField('Zip Code', validators=[Required()])
    submit = SubmitField('Update Profile')


def validate_stage(self, field):
    if self.state == 'NONE':
        raise ValidationError("Please select a State!")


class UsernameForm(FlaskForm):
    """ Form for password reset """
    username = StringField(
        'Username', [Email(), Required(), Length(min=6, max=50)])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError("Account does not exist!")


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')
