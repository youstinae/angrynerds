from flask import Blueprint, render_template

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


@public.route('/contact')
def contact():
    return render_template('contact.html')
