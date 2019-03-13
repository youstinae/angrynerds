from flask import Blueprint, render_template
from flask_security import (Security, login_required,
                            SQLAlchemySessionUserDatastore)


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')
