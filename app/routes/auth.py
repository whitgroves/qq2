from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from app.extensions import db
from app.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register() -> str:
    match request.method:
        case 'GET':
            return render_template('register.html')
        case 'POST':
            email = request.form['email'].strip()
            password = request.form['password'].strip()
            username = request.form['username'].strip()
            errors = False
            if any(len(x) == 0 for x in [email, password, username]):
                flash('Please fill out all fields.')
                errors = True
            if len(User.query.filter_by(email=email).all()) > 0:
                flash('Email must be unique.')
                errors = True
            if errors:
                return render_template('register.html', email=email, username=username)
            else:
                password = generate_password_hash(password)
                user = User(email=email, password=password, username=username)
                db.session.add(user)
                db.session.commit()
                user = User.query.filter_by(email=email).first()
                flash('New user registered.')
                return redirect(url_for('users.user', id=user.id))                             
        case _:
            abort(400)

@bp.route('/login', methods=('GET', 'POST'))
def login() -> str:
    match request.method:
        case 'GET':
            return render_template('login.html')
        case 'POST':
            user_email = request.form['user_email'].strip()
            password = request.form['password'].strip()
            remember = 'remember' in request.form.keys()
            errors = 0
            user = User.query.filter(db.or_(User.email==user_email, User.username==user_email)).first()
            if not user or not check_password_hash(user.password, password):
                flash('Invalid credentials.')
                errors += 1
            if errors > 0:
                return render_template('login.html', user_email=user_email)
            else:
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