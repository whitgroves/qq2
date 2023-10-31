"""Routes for post operations in qq2. Deprecated."""
import flask
import flask_login
from app import models, forms
from app import extensions as ext

bp = flask.Blueprint('posts', __name__)

@bp.route('/')
def index():
    """Returns all posts."""
    posts = models.Post.query.all()
    return flask.render_template('posts/index.html', posts=posts)

@bp.route('/<int:_id>')
def get_post(_id):
    """Returns the post specified by <_id>."""
    post = ext.db.session.get(models.Post, _id)
    if not post:
        return flask.redirect(flask.url_for('posts.index'))
    form = forms.CommentForm()
    return flask.render_template('posts/post.html', post=post, form=form)

@bp.route('/tags/')
def get_tags():
    """Returns all tags."""
    tags = models.Tag.query.all()
    return flask.render_template('posts/tags.html', tags=tags)

@bp.route('/tags/<name>')
def get_tag(name):
    """Returns all posts for tag <name>."""
    tag = models.Tag.query.filter_by(name=name).first_or_404()
    return flask.render_template('posts/tag.html', tag=tag)

@bp.route('/comments/')
def get_comments():
    """Returns all comments."""
    comments = models.Comment.query.all()
    return flask.render_template('posts/comments.html', comments=comments)

@bp.post('/<int:_id>/comments/add/')
@flask_login.login_required
def add_comment(_id):
    """Adds a comment to the post specified by <_id>."""
    post = models.Post.query.filter_by(id=_id).first_or_404()
    form = forms.CommentForm()
    content = form.content.data
    errors = False
    code = 400 # catch errors for testing
    if content is None or len(content) == 0:
        flask.flash("Can't reply with empty comment.")
        errors = True
    if not errors and form.validate_on_submit():
        comment = models.Comment(content=content.strip(),
                                 post=post,
                                 user=flask_login.current_user)
        ext.db.session.add(comment)
        ext.db.session.commit()
        code = 302 # default for redirect()
    return flask.redirect(flask.url_for('posts.get_post', _id=post.id), code=code)

@bp.post('/comments/<int:_id>/delete/')
@flask_login.login_required
def delete_comment(_id):
    """Deletes the comment specified by <_id>."""
    comment = models.Comment.query.filter_by(id=_id).first_or_404()
    if comment.user.id != flask_login.current_user.id:
        flask.abort(403)
    post_id = comment.post.id
    ext.db.session.delete(comment)
    ext.db.session.commit()
    return flask.redirect(flask.url_for('posts.get_post', _id=post_id))
