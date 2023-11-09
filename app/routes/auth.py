"""Routes for user authentication in qq2."""
import flask
import flask_login
import werkzeug.security as ws
from app import models, forms
from app import extensions as ext

bp = flask.Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register() -> flask.Response:
    """Handles user registrations."""
    form = forms.RegisterForm()
    match flask.request.method:
        case 'GET':
            return flask.render_template('register.html', form=form)
        case 'POST':
            email = form.email.data.strip()
            password = form.password.data.strip()
            username = form.username.data.strip()
            errors = False
            if len(models.User.query.filter_by(email=email).all()) > 0:
                flask.flash('Email must be unique.')
                errors = True
            if not errors and form.validate_on_submit():
                password = ws.generate_password_hash(password)
                user = models.User(email=email,
                                   password=password,
                                   username=username)
                ext.db.session.add(user)
                ext.db.session.commit()
                msg = f'New user registered: "{user.username}" ({user.email}).'
                flask.current_app.logger.info(msg)
                flask.flash(msg)
                return flask.redirect(flask.url_for('auth.login'))
            return flask.render_template('register.html', form=form), 400
        case _:
            flask.current_app.logger.warn(
                f'405: /auth/register: {flask.request.method}: {flask.request}')
            flask.abort(405)

@bp.route('/login', methods=('GET', 'POST'))
def login() -> flask.Response:
    """Handles user login."""
    form = forms.LoginForm()
    match flask.request.method:
        case 'GET':
            return flask.render_template('login.html', form=form)
        case 'POST':
            user_email = form.user_email.data.strip()
            password = form.password.data.strip()
            remember = form.remember.data
            errors = False
            user = models.User.query.filter(ext.db.or_(
                models.User.email==user_email,
                models.User.username==user_email)).first()
            if not user or not ws.check_password_hash(user.password, password):
                flask.flash('Invalid credentials.')
                errors = True
            if not errors and form.validate_on_submit():
                flask_login.login_user(user, remember=remember)
                msg = f'User "{user.username}" ({user.email}) logged in.'
                flask.current_app.logger.info(msg)
                flask.flash(msg)
                return flask.redirect(flask.url_for('main.index'))
            return flask.render_template('login.html', form=form), 400
        case _:
            flask.current_app.logger.warn(
                f'405: /auth/login: {flask.request.method}: {flask.request}')
            flask.abort(405)

@flask_login.login_required
@bp.route('/logout')
def logout() -> flask.Response:
    """Logs the current user out."""
    name = flask_login.current_user.username
    flask_login.logout_user()
    flask.flash(f'User {name} was logged out.')
    return flask.redirect(flask.url_for('main.index'))
