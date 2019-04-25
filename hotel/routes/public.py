from flask import Blueprint, flash, redirect, render_template, request, url_for

from hotel.db import db
from hotel.forms.booking import BookingForm
from hotel.forms.contact import ContactForm
from hotel.forms.feedback import FeedbackForm
from hotel.forms.newsletter import NewsletterForm
from hotel.forms.payment import PaymentForm
from hotel.models import Contact, Feedback, Newsletter, Payment

public = Blueprint('public', __name__, url_prefix='/')


@public.route('/')
@public.route('/home')
def index():
    return render_template('index.html')


@public.route('/about')
def about():
    return render_template('about.html')


@public.route('/accomodation')
def accomodation():
    return render_template('accomodation.html')


@public.route('/accomodation2')
def accomodation2():
    return render_template('accomodation2.html')


@public.route('/standardq')
def standardq():
    return render_template('standard_queen.html')


@public.route('/rooms/deluxedouble')
def doubleq():
    return render_template('public/deluxe_double.html')


@public.route('/kingsuite')
def kingsuite():
    return render_template('public/king_suite.html')


@public.route('/familysuite')
def familysuite():
    return render_template('public/family_suite.html')


@public.route('/gallery')
def gallery():
    return render_template('gallery.html')


@public.route('/elements')
def elements():
    return render_template('elements.html')


@public.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    """ newsletter sign up """
    form = NewsletterForm()
    if request.method == 'POST':
        # result = request.form
        if form.validate_on_submit():
            newsl = Newsletter()
            newsl.first_name = form.first_name.data
            newsl.last_name = form.last_name.data
            newsl.email = form.email.data
            db.session.add(newsl)
            db.session.commit()
            return redirect(url_for('public.newsletter_confirm'))

    return render_template('newsletter/index.html', form=form)


@public.route('/newsletter/confirm')
def newsletter_confirm():
    return render_template('newsletter/confirm.html')


@public.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = ContactForm()
    if form.validate_on_submit():
        fb = Contact()
        fb.name = form.name.data
        fb.email = form.email.data
        fb.subject = form.subject.data
        fb.message = form.message.data
        fb.type = 'FEED'
        db.session.add(fb)
        db.session.commit()
        flash('Your message has been sent!')
        return redirect(url_for('public.feedback'))
    return render_template('feedback.html', form=form, title='Feedback')


@public.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Handle requests to the /contactus route
    Add an user to the database through the registration form
    """
    form = ContactForm()
    if form.validate_on_submit():
        info = Contact()
        info.name = form.name.data
        info.email = form.email.data
        info.subject = form.subject.data
        info.message = form.message.data
        db.session.add(info)
        db.session.commit()
        flash('Your message has been sent!')
        return redirect(url_for('public.contact'))
    return render_template('contact.html', form=form, title='Contact')


@public.route('/payment', methods=['GET', 'POST'])
def payment():
    """ Handle requests to the /payments route """
    form = PaymentForm()
    if form.is_submitted():
        if not form.validate_on_submit():
            flash('Information Not Valid')
    if form.validate_on_submit():
        payinfo = Payment()
        payinfo.name = form.name.data
        payinfo.cardNumber = form.cardNumber.data
        payinfo.month = form.month.data
        payinfo.year = form.year.data
        payinfo.cvv = form.cvv.data
        db.session.add(payinfo)
        db.session.commit()
        flash('Payment Successful')
        return redirect(url_for('public.payment'))

    return render_template('payment.html', form=form, title='Payment')


@public.route('/booking', methods=['GET', 'POST'])
def booking():
    """
    Handle requests to the /booking route
    Add a booking to the database
    """
    form = BookingForm()
    if form.validate_on_submit():
        bf = BookingForm()
        bf.arrival = form.datetimepicker11.data
        bf.departure = form.datetimepicker1.data
        bf.adults = form.adult.data
        bf.child = form.child.data
        bf.rooms = form.room.data
        db.session.add(bf)
        db.session.commit()
        return redirect(url_for('public.standardq'))
    return render_template('public/standard_queen.html', form=form, title='Booking')
