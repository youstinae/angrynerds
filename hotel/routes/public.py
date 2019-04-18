from flask import Blueprint, flash, redirect, render_template, url_for

from hotel.db import db
from hotel.forms.contact import ContactForm
from hotel.forms.feedback import FeedbackForm
from hotel.models import Contact, Feedback


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

@public.route('/standardqueen')
def standardq():
    return render_template('standardqueen.html')

@public.route('/gallery')
def gallery():
    return render_template('gallery.html')


@public.route('/elements')
def elements():
    return render_template('elements.html')


@public.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        feedback = Feedback(name=name,
                            email=email,
                            subject=subject,
                            message=message)
        db.session.add(feedback)
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
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        contact = Contact(name=name,
                          email=email,
                          subject=subject,
                          message=message)
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been sent!')
        return redirect(url_for('public.contact'))
    return render_template('contact.html', form=form, title='Contact')
