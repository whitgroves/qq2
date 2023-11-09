"""Routes for CRUD operations on users in qq2."""
import flask
import flask_login
from app import models, forms
from app import extensions as ext

bp = flask.Blueprint('users', __name__)

@bp.route('/')
def index() -> flask.Response:
    """Returns a list of all users."""
    users = models.User.query.all()
    return flask.render_template('users/index.html', users=users)

@bp.route('/<int:id_>')
def get_user(id_:int) -> flask.Response:
    """Returns a specific user's profile."""
    user = ext.db.session.get(models.User, id_)
    if not user:
        return flask.redirect(flask.url_for('users.index'))
    return flask.render_template('users/user.html', user=user)

@bp.route('/<int:id_>/edit', methods=('GET', 'POST'))
@flask_login.login_required
def edit_user(id_:int) -> flask.Response:
    """Handles user profile updates."""
    if id_ != flask_login.current_user.id:
        flask.abort(403)
    user = ext.db.session.get(models.User, id_)
    if not user:
        return flask.redirect(flask.url_for('users.index'), code=403)
    form = forms.UserForm()
    match flask.request.method:
        case 'GET':
            return flask.render_template('users/edit.html',
                                         user=user,
                                         form=form)
        case 'POST':
            username = form.username.data or user.username
            email = form.email.data or user.email
            bio = form.bio.data or user.bio
            errors = False
            if len(models.User.query.filter_by(email=email).all()) > \
                    int(user.email == email): # email change = 0, no change = 1
                flask.flash('Email must be unique.')
                errors = True
            if not errors and form.validate_on_submit():
                user.username = username
                user.email = email
                user.bio = bio
                ext.db.session.add(user)
                ext.db.session.commit()
                flask.flash(f'User {username} updated successfully.')
                return flask.redirect(flask.url_for('users.get_user',
                                                    id_=user.id))
            return flask.render_template('users/edit.html',
                                         user=user,
                                         form=form), 400
        case _:
            flask.abort(405)

@bp.post('/<int:id_>/delete/')
@flask_login.login_required
def delete_user(id_:int) -> flask.Response:
    """Handles user profile deletions."""
    if id_ != flask_login.current_user.id:
        flask.abort(403)
    user = models.User.query.get_or_404(id_)
    ext.db.session.delete(user)
    ext.db.session.commit()
    return flask.redirect(flask.url_for('users.index'))
