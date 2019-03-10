from flask import request, render_template

from . import home


@home.route('/')
@home.route('/home')
def home():
    return render_template('index.html')


@home.route('/about')
def about():
    return render_template('about.html')


@home.route('/accomodation')
def accomodation():
    return render_template('accomodation.html')


@home.route('/gallery')
def gallery():
    return render_template('gallery.html')


@home.route('/elements')
def elements():
    return render_template('elements.html')


@home.route('/contact')
def contact():
    return render_template('contact.html')


@home.errorhandler(404)
def not_found(error):
    home.logger.error('Page not found: %s', (request.path, error))
    return render_template('error_404.html'), 404


@home.errorhandler(500)
def internal_server_error(error):
    home.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500


@home.errorhandler(Exception)
def unhandled_exception(error):
    home.logger.error('Unhandled Exception: %s', (error))
    return render_template('error_500.html'), 500
