"""Routes for post operations in qq2."""
import flask
import flask_login
from app import models, forms
from app import extensions as ext

bp = flask.Blueprint('posts', __name__)

@bp.route('/')
def index() -> flask.Response:
    """Returns all posts."""
    posts = models.Post.query.all()
    flask.current_app.logger.debug(flask_login.current_user)
    return flask.render_template('posts/index.html',
                                 posts=posts,
                                 user=flask_login.current_user)

@bp.route('/<int:id_>')
def get_post(id_:int) -> flask.Response:
    """Returns the post specified by <id_>."""
    post = ext.db.session.get(models.Post, id_)
    if not post: return flask.redirect(flask.url_for('posts.index'))
    form = forms.CommentForm()
    return flask.render_template('posts/post.html', post=post, form=form)

@flask_login.login_required
@bp.route('/new', methods=('GET', 'POST'))
def new_post() -> flask.Response:
    """Creates a new post."""
    form = forms.PostForm()
    match flask.request.method:
        case 'GET':
            return flask.render_template('posts/new.html', form=form)
        case 'POST':
            title = form.title.data.strip()
            content = form.content.data.strip()
            tags = [models.Tag(name='TODO'),
                    models.Tag(name='NotImplementedException')]
            if form.validate_on_submit():
                post = models.Post(title=title,
                                   content=content,
                                   user_id=flask_login.current_user.id,
                                   tags=tags)
                ext.db.session.add(post)
                ext.db.session.commit()
                flask.current_app.logger.debug(f'New post: {post}')
                return flask.redirect(flask.url_for('posts.index'))
            return flask.render_template('posts/new.html', form=form), 400
        case _:
            flask.current_app.logger.warn(
                f'405: /posts/new: {flask.request.method}: {flask.request}')
            flask.abort(405)


@flask_login.login_required
@bp.route('/<int:id_>/edit', methods=('GET', 'POST'))
def edit_post(id_:int) -> flask.Response:
    """Updates the post specified by <id_> if the current user wrote it."""
    post = ext.db.session.get(models.Post, id_)
    if not post:
        return flask.redirect(flask.url_for('posts.index'), code=403)
    if post.user_id != flask_login.current_user.id:
        flask.abort(403)
    form = forms.PostForm()
    match flask.request.method:
        case 'GET':
            return flask.render_template('posts/edit.html',
                                         post=post,
                                         form=form)
        case 'POST':
            if form.validate_on_submit():
                post.title = form.title.data.strip() or post.title
                post.content = form.content.data.strip() or post.content
                # post.tags = form.tags.data
                ext.db.session.add(post)
                ext.db.session.commit()
                return flask.redirect(flask.url_for('posts.get_post',
                                      id_=post.id))
            return flask.render_template('posts/edit.html',
                                         post=post,
                                         form=form), 400
        case _:
            flask.current_app.logger.warn(
                f'405: /posts/new: {flask.request.method}: {flask.request}')
            flask.abort(405)

@bp.route('/tags/')
def get_tags() -> flask.Response:
    """Returns all tags."""
    tags = models.Tag.query.all()
    return flask.render_template('posts/tags.html', tags=tags)

@bp.route('/tags/<name>')
def get_tag(name:str) -> flask.Response:
    """Returns all posts for tag <name>."""
    tag = models.Tag.query.filter_by(name=name).first_or_404()
    return flask.render_template('posts/tag.html', tag=tag)

@bp.route('/comments/')
def get_comments() -> flask.Response:
    """Returns all comments."""
    comments = models.Comment.query.all()
    return flask.render_template('posts/comments.html', comments=comments)

@flask_login.login_required
@bp.post('/<int:id_>/comments/add/')
def add_comment(id_:int) -> flask.Response:
    """Adds a comment to the post specified by <id_>."""
    post = models.Post.query.filter_by(id=id_).first_or_404()
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
    return flask.redirect(flask.url_for('posts.get_post', id_=post.id),
                          code=code)

@flask_login.login_required
@bp.post('/comments/<int:id_>/delete/')
def delete_comment(id_:int) -> flask.Response:
    """Deletes the comment specified by <id_>."""
    comment = models.Comment.query.filter_by(id=id_).first_or_404()
    if comment.user.id != flask_login.current_user.id:
        flask.abort(403)
    post_id = comment.post.id
    ext.db.session.delete(comment)
    ext.db.session.commit()
    return flask.redirect(flask.url_for('posts.get_post', id_=post_id))
