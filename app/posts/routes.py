from flask import render_template
from app.posts import bp
from app.extensions import db
from app.models.post import Post
from app.models.comment import Comment
from app.models.tag import Tag

@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)

@bp.route('/tags/')
def tags():
    tags = Tag.query.all()
    return render_template('posts/tags.html', tags=tags)

@bp.route('/tags/<name>/')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('posts/tag.html', tag=tag)