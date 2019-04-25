""" contact form """

from flask_security.forms import Length
from flask_wtf import FlaskForm
from wtforms import BooleanField, Form, StringField, TextField, validators
from wtforms.fields.core import DateTimeField
from wtforms.fields.simple import SubmitField
from wtforms.validators import Required


class BookingForm(FlaskForm):
    arrival = DateTimeField('Arrival', [Required()])

    departure = DateTimeField('Departure', [Required()])

    adults = StringField(
        'Adults', [Required(), Length(min=0, max=1)])

    children = StringField(
        'Child', [Required(), Length(min=0, max=1)])

    rooms = StringField(
        'Rooms', [Required(), Length(min=0, max=1)])

    submit = SubmitField('Book Now')
