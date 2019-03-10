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


@public.errorhandler(404)
def not_found(error):
    # logger.error('Page not found: %s', (request.path, error))
    return render_template('error_404.html'), 404


@public.errorhandler(500)
def internal_server_error(error):
    # logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500


@public.errorhandler(Exception)
def unhandled_exception(error):
    # @public.logger.error('Unhandled Exception: %s', (error))
    return render_template('error_500.html'), 500
