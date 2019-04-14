""" blog routes """

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)

from hotel.db import db
from hotel.models import Post, Tag

blog = Blueprint('blog', __name__, url_prefix='/blog')


@blog.route('/')
def index():
    """ Show all the posts, most recent first """
    posts = Post.query.all()
    tags = Tag.query.all()
    return render_template('blog/index.html', posts=posts, tags=tags)


@blog.route('/tag/<int:id>', methods=["GET"])
def get_by_tag(id):
    """ get a post by id """
    posts = Post.query.filter(Post.tags.any(id=id)).all()
    tags = Tag.query.all()
    return render_template('blog/index.html', posts=posts, tags=tags)


def udpate_view_count(id):
    post = Post.query.filter_by(id=id).first()
    post.view_count += 1
    db.session.commit()


@blog.route('/create', methods=('GET', 'POST'))
# @login_required
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


@blog.route('/<int:id>', methods=["GET"])
def get(id):
    """ get a post by id """
    post = Post.query.filter_by(id=id).first()
    tags = Tag.query.all()
    if not post:
        flash('invalid post id')
        render_template('blog/index.html')
    udpate_view_count(id)
    return render_template('blog/post.html', post=post, tags=tags)


def udpate_view_count(id):
    post = Post.query.filter_by(id=id).first()
    post.view_count += 1
    db.session.commit()


@blog.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
def update():
    """ Update a post if the current user is the author """
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = get_post(id)
            post.title = title
            post.body = body
            db.session.update(post)
            db.session.commit()
            db.session.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@blog.route('/<int:id>/delete', methods=('POST',))
# @login_required
def delete():
    """
    Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    db.session.close()
    return redirect(url_for('blog.index'))


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
