from flask import Blueprint, flash, redirect, render_template, url_for

from hotel.db import db
from hotel.forms.contact import ContactForm
from hotel.models import Contact

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


@public.route('/gallery')
def gallery():
    return render_template('gallery.html')


@public.route('/elements')
def elements():
    return render_template('elements.html')


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
        return redirect(url_for('public.index'))
    else:
        flash('form is not valid: %s' % form.errors.items())
    return render_template('contact.html', form=form, title='Register')
