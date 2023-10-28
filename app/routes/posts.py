from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from app.extensions import db
from app.models.posts import Post, Tag, Comment
from app.forms import CommentForm
from flask_login import login_required, current_user

bp = Blueprint('posts', __name__)

@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)

@bp.route('/<int:id>')
def post(id):
    post = db.session.get(Post, id)
    if not post:
        return redirect(url_for('posts.index'))
    form = CommentForm()
    return render_template('posts/post.html', post=post, form=form)

@bp.route('/tags/')
def tags():
    tags = Tag.query.all()
    return render_template('posts/tags.html', tags=tags)

@bp.route('/tags/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('posts/tag.html', tag=tag)

@bp.route('/comments/')
def comments():
    comments = Comment.query.all()
    return render_template('posts/comments.html', comments=comments)

@bp.post('/<int:id>/comments/add/')
@login_required
def add_comment(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    content = form.content.data
    errors = False
    code = 400 # catch errors for testing
    if content is None or len(content) == 0:
        flash("Can't reply with empty comment.")
        errors = True
    if not errors and form.validate_on_submit():
        comment = Comment(content=content.strip(), post=post, user=current_user)
        db.session.add(comment)
        db.session.commit()
        code = 302 # default for redirect()
    return redirect(url_for('posts.post', id=post.id), code=code)

@bp.post('/comments/<int:id>/delete/')
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first_or_404()
    if comment.user.id != current_user.id:
        abort(403)
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('posts.post', id=post_id))
