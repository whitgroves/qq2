from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.extensions import db
from app.models.users import User
from app.forms import UserForm
from flask_login import login_required, current_user

bp = Blueprint('users', __name__)

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@bp.route('/<int:id>')
def user(id):
    user = db.session.get(User, id)
    if not user:
        return redirect(url_for('users.index'))
    return render_template('users/user.html', user=user)

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    if id != current_user.id:
        abort(403)
    user = db.session.get(User, id)
    if not user:
        return redirect(url_for('users.index'), code=403)
    form = UserForm()
    match request.method:
        case 'GET':
            return render_template('users/edit.html', user=user, form=form)
        case 'POST':
            username = form.username.data or user.username
            email = form.email.data or user.email
            bio = form.bio.data or user.bio
            errors = False
            if len(User.query.filter_by(email=email).all()) > int(user.email == email):
                flash('Email must be unique.')
                errors = True
            if not errors and form.validate_on_submit():
                user.username = username
                user.email = email
                user.bio = bio
                db.session.add(user)
                db.session.commit()
                flash(f'User {username} updated successfully.')
                return redirect(url_for('users.edit', id=user.id))
            else:
                return render_template('users/edit.html', user=user, form=form), 400
        case _:
            abort(405)

@bp.post('/<int:id>/delete/')
@login_required
def delete(id):
    if id != current_user.id:
        abort(403)
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.index'))
