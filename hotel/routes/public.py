from flask import Blueprint, flash, redirect, render_template, url_for

from hotel.db import db
from hotel.forms.contact import ContactForm
from hotel.forms.feedback import FeedbackForm
from hotel.forms.newsletter import NewsletterForm
from hotel.models import Contact, Feedback, Newsletter

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


@public.route('/newsletter', methods=['POST'])
def newsletter():
    """
    newsletter sign up
    """
    form = NewsletterForm()
    if form.validate_on_submit():
        nl = Newsletter()
        nl.email = form.email.data
        db.session.add(nl)
        db.session.commit()
        flash('Congratulations on signing up for our newsletter!')
        return redirect(url_for('public.index'))
    return render_template('index.html')


@public.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        fb = Feedback()
        fb.name = form.name.data
        fb.email = form.email.data
        fb.subject = form.subject.data
        fb.message = form.message.data
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
