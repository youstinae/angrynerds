""" admin module """

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import current_user, login_required

from hotel.db import db
from hotel.forms.post import PostUpdateForm
from hotel.forms.profile import ProfileForm
from hotel.models import Post

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/cancel')
def cancel():
    return render_template('admin/cancel.html')


@admin.route('/cancel_account', methods=['POST'])
@login_required
def cancel_account():
    """ cancel user account """
    user = current_user
    user.cancelled = True
    db.session.commit()
    flash('Your account has been cancelled!')
    return redirect(url_for('auth.login'))


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
    db.session.commit()
    return redirect(url_for('admin.posts'))


@admin.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """ Create a new post for the current user """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            post = Post(title=title, bogy=body, author_id=g.user['id'])
            db.session.add(post)
            db.session.commit()
            db.session.close()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


@admin.route('/posts/<int:id>/update', methods=['GET', 'POST'])
@login_required
def post_update(id):
    """ Update a post """
    post = Post.query.get(id)
    form = PostUpdateForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.summary = form.summary.data
        post.content = form.content.data
        post.image_feature1 = form.image_feature1.data
        post.image_feature2 = form.image_feature2.data
        post.image_feature3 = form.image_feature3.data
        post.published = form.published.data
        db.session.commit()
        return redirect(url_for('admin.posts'))
    form.title.data = post.title
    form.summary.data = post.summary
    form.content.data = post.content
    form.image_feature1.data = post.image_feature1
    form.image_feature2.data = post.image_feature2
    form.image_feature3.data = post.image_feature3
    form.published.data = post.published
    return render_template('admin/blog_update.html', form=form, post=post)
