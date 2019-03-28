from flask import Blueprint, render_template
from flask_security import login_required


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/profile')
@login_required
def profile():
    return render_template('admin/profile.html')
