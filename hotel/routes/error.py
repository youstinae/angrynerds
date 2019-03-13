from logging import log

from flask import Blueprint, render_template, request

error = Blueprint('error', __name__, url_prefix='/error')


@error.errorhandler(404)
def error_404(error):
    log.error('Page not found: %s', (request.path, error))
    return render_template('error_404.html'), 404


@error.errorhandler(500)
def error_500(error):
    log.error('Server Error: %s', (error))
    return render_template('500.html'), 500


@error.errorhandler(Exception)
def error_unhandled(error):
    log.error('Unhandled Exception: %s', (error))
    return render_template('error_500.html'), 500
