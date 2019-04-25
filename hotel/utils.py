""" utility module """

import datetime
import os
import random
from urllib.parse import urljoin, urlparse

from flask import redirect, request, url_for


def get_app_base_path():
    return os.path.abspath(os.path.dirname(__file__))


def get_instance_folder_path():
    return os.path.join(get_app_base_path(), 'instance')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


def get_random_date(year):
    # try to get a date
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y')
    # if the value happens to be in the leap year range, try again
    except ValueError:
        get_random_date(year)
