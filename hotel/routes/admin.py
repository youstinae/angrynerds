from flask import Blueprint, flash, redirect, render_template, url_for
from flask_security import current_user, login_required

from hotel.db import db
from hotel.forms.profile import ProfileForm
from hotel.models import Post

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zipcode = form.zipcode.data
        db.session.commit()
        flash('Your profile have been updated.')
        return redirect(url_for('admin.profile'))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.email.data = current_user.email
    form.address.data = current_user.address
    form.city.data = current_user.city
    form.state.data = current_user.state
    form.zipcode.data = current_user.zipcode
    return render_template('admin/profile.html', form=form)


@admin.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    return render_template('admin/blog_posts.html', posts=posts)


@admin.route('/posts/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    """ deletes a post """
    post = Post.query.get(id)
    post.published = False
    post.deleted = True
    db.session.commit()
    return redirect(url_for('admin.posts'))
