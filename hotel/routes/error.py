from logging import log

from flask import Blueprint, render_template, request

error = Blueprint('error', __name__, url_prefix='/error')


@error.errorhandler(403)
def error_403(error):
    log.error('Forbidden: %s', (request.path, error))
    return render_template('error/error_403.html'), 403


@error.errorhandler(404)
def error_404(error):
    log.error('Page not found: %s', (request.path, error))
    return render_template('error/error_404.html'), 404


@error.errorhandler(500)
def error_500(error):
    log.error('Server Error: %s', (error))
    return render_template('error/error_500.html'), 500


@error.errorhandler(Exception)
def error_ex(error):
    log.error('Unhandled Exception: %s', (error))
    return render_template('error/error_ex.html'), 500
