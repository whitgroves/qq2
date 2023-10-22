from flask import render_template, request, flash, redirect, url_for
from app.posts import bp
from app.extensions import db
from app.models.posts import Post, Tag, Comment

@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)

@bp.route('/<int:id>/')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/post.html', post=post)

@bp.route('/tags/')
def tags():
    tags = Tag.query.all()
    return render_template('posts/tags.html', tags=tags)

@bp.route('/tags/<name>/')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('posts/tag.html', tag=tag)

@bp.route('/comments/')
def comments():
    comments = Comment.query.all()
    return render_template('posts/comments.html', comments=comments)

@bp.post('/<int:id>/comment/')
def add_comment(id):
    post = Post.query.get_or_404(id)
    content = request.form['content']
    if len(content) == 0:
        flash('Comment cannot be blank.')
    else:
        comment = Comment(content=content, post=post)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('posts.post', id=post.id))

@bp.post('/comment/<int:id>/delete/')
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('posts.post', id=post_id))