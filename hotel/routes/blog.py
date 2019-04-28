""" blog routes """

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   url_for)

from hotel.db import db
from hotel.forms.comment import CommentForm
from hotel.models import Comment, Post, Tag

blog = Blueprint('blog', __name__, url_prefix='/blog')


@blog.route('/')
def index():
    """ Show all the posts, most recent published first """
    posts = Post.query.filter_by(published=True).order_by(
        Post.publish_date.desc()).paginate(per_page=5)
    tags = Tag.query.all()
    pops = Post.query.order_by(Post.view_count.desc()).limit(5).all()
    return render_template('blog/index.html', posts=posts, tags=tags, pops=pops)


@blog.route('/tag/<int:id>', methods=['GET'])
def get_by_tag(id):
    """ get a post by id """
    posts = Post.query.filter_by(published=True).filter(
        Post.tags.any(id=id)).order_by(
        Post.publish_date.desc()).paginate(per_page=5)
    tags = Tag.query.all()
    pops = Post.query.order_by(Post.view_count.desc()).limit(5).all()
    return render_template('blog/index.html', posts=posts, tags=tags, pops=pops)


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


def udpate_view_count(id):
    post = Post.query.filter_by(id=id).first()
    post.view_count += 1
    db.session.commit()
