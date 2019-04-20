""" blog routes """

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)

from hotel.db import db
from hotel.forms.comment import CommentForm
from hotel.models import Comment, Post, Tag

blog = Blueprint('blog', __name__, url_prefix='/blog')


@blog.route('/')
def index():
    """ Show all the posts, most recent first """
    posts = Post.query.filter_by(published=True).all()
    tags = Tag.query.all()
    return render_template('blog/index.html', posts=posts, tags=tags)


@blog.route('/tag/<int:id>', methods=['GET'])
def get_by_tag(id):
    """ get a post by id """
    posts = Post.query.filter_by(published=True).filter(
        Post.tags.any(id=id)).all()
    tags = Tag.query.all()
    return render_template('blog/index.html', posts=posts, tags=tags)


@blog.route('/<int:id>', methods=['GET'])
def get(id):
    """ get a post by id """
    form = CommentForm()
    post = Post.query.filter_by(id=id).first()
    tags = Tag.query.all()
    if not post:
        flash('invalid post id')
        render_template('blog/index.html')
    udpate_view_count(id)
    return render_template('blog/post.html', form=form, post=post, tags=tags)


@blog.route('/<int:id>/comment', methods=['POST'])
def comment(id):
    """ comment on a blog post """
    form = CommentForm()
    post = Post.query.filter_by(id=id).first()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        comm = Comment(name=name, email=email,
                       content=message, post_id=post.id)
        post.comments.append(comm)
        db.session.commit()
        return redirect(url_for('blog.get', id=id))
    return render_template('blog/post.html', form=form, post=post)


def get_post(check_author=True):
    """
    Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = Post.query.filter_by(id=id).first()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


def udpate_view_count(id):
    post = Post.query.filter_by(id=id).first()
    post.view_count += 1
    db.session.commit()
