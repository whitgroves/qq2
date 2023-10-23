from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from app.extensions import db
from app.models.users import User
from app.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register() -> str:
    form = RegisterForm()
    match request.method:
        case 'GET':
            return render_template('register.html', form=form)
        case 'POST':
            email = form.email.data.strip()
            password = form.password.data.strip()
            username = form.username.data.strip()
            if len(User.query.filter_by(email=email).all()) > 0:
                flash('Email must be unique.')
                return render_template('register.html', form=form)
            if form.validate_on_submit():
                password = generate_password_hash(password)
                user = User(email=email, password=password, username=username)
                db.session.add(user)
                db.session.commit()
                user = User.query.filter_by(email=email).first()
                flash('New user registered.')
                return redirect(url_for('auth.login'))                             
        case _:
            abort(400)

@bp.route('/login', methods=('GET', 'POST'))
def login() -> str:
    form = LoginForm()
    match request.method:
        case 'GET':
            return render_template('login.html', form=form)
        case 'POST':
            user_email = form.user_email.data.strip()
            password = form.password.data.strip()
            remember = form.remember.data
            user = User.query.filter(db.or_(User.email==user_email, User.username==user_email)).first()
            if not user or not check_password_hash(user.password, password):
                flash('Invalid credentials.')
                return render_template('login.html', form=form)
            if form.validate_on_submit():
                login_user(user, remember=remember)
                flash(f'User {user.username} logged in successfully.')
                return redirect(url_for('main.index'))
        case _:
            abort(400)

@bp.route('/logout')
@login_required
def logout() -> str:
    name = current_user.username
    logout_user()
    flash(f'User {name} was logged out.')
    return redirect(url_for('main.index'))