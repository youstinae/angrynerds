""" payment form """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Email, Length, Required, NumberRange


class PaymentForm(FlaskForm):
    """
    Form for submiting a contact form
    """
    name = StringField(
        'Name', [Required(), Length(min=2, max=50)])
            
    cardNumber = StringField(
        'cardNumber', [Required(), Length(min=16, max=16)])

    month = IntegerField(
        'month', [Required()])
    
    year = IntegerField(
        'year', [Required()])

    cvv = IntegerField(
        'cvv', [Required()])

    submit = SubmitField(' Confirm  ')
