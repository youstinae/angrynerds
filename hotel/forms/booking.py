""" contact form """

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField,StringField, TextField, validators



class BookingForm(FlaskForm):
    
    arrival = DateTimeField(
        'Arrival', [Required(), format='%Y-%m-%d %H:%M:%S')

    departure = DateTimeField(
        'Departure', [Required(), format='%Y-%m-%d %H:%M:%S')

    adults = StringField(
        'Adults', [Required(), Length(min=0, max=1)])

    child = StringField(
        'Child', [Required(), Length(min=0, max=1)])

    rooms = StringField(
        'Rooms', [Required(), Length(min=0, max=1)])

    submit = SubmitField('Book Now')
