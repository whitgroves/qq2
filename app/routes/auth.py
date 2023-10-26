from flask import Blueprint, request, current_app, render_template, flash, redirect, url_for, abort, Response
from app.extensions import db
from app.models.users import User
from app.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register() -> Response:
    form = RegisterForm()
    match request.method:
        case 'GET':
            return render_template('register.html', form=form)
        case 'POST':
            email = form.email.data.strip()
            password = form.password.data.strip()
            username = form.username.data.strip()
            errors = False
            if len(User.query.filter_by(email=email).all()) > 0:
                flash('Email must be unique.')
                errors = True
            if not errors and form.validate_on_submit():
                password = generate_password_hash(password)
                user = User(email=email, password=password, username=username)
                db.session.add(user)
                db.session.commit()
                msg = f'New user registered: "{user.username}" ({user.email}).'
                current_app.logger.info(msg)
                flash(msg)
                return redirect(url_for('auth.login'))
            else:
                return render_template('register.html', form=form), 400                           
        case _:
            current_app.logger.warn(f'Unexpected request @ /register: {request.method} : {request}')
            abort(405)

@bp.route('/login', methods=('GET', 'POST'))
def login() -> Response:
    form = LoginForm()
    match request.method:
        case 'GET':
            return render_template('login.html', form=form)
        case 'POST':
            user_email = form.user_email.data.strip()
            password = form.password.data.strip()
            remember = form.remember.data
            errors = False
            user:User = User.query.filter(db.or_(User.email==user_email, User.username==user_email)).first()
            if not user or not check_password_hash(user.password, password):
                flash('Invalid credentials.')
                errors = True
            if not errors and form.validate_on_submit():
                login_user(user, remember=remember)
                msg = f'User "{user.username}" ({user.email}) logged in successfully.'
                current_app.logger.info(msg)
                flash(msg)
                return redirect(url_for('main.index'))
            else:
                return render_template('login.html', form=form), 400
        case _:
            current_app.logger.warn(f'Unexpected request @ /login: {request.method} : {request}')
            abort(405)

@bp.route('/logout')
@login_required
def logout() -> Response:
    name = current_user.username
    logout_user()
    flash(f'User {name} was logged out.')
    return redirect(url_for('main.index'))
