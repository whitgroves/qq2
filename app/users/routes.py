from flask import render_template, request, redirect, url_for, flash
from app.users import bp
from app.extensions import db
from app.models.users import User

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@bp.route('/<int:id>/')
def user(id):
    user = User.query.get_or_404(id)
    return render_template('users/user.html', user=user)

@bp.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        bio = request.form['bio']
        errors = False
        if len(User.query.filter_by(username=username).all()) > int(user.username == username):
            flash('Username should be unique.')
            errors = True
        if len(User.query.filter_by(email=email).all()) > int(user.email == email):
            flash('Email must be unique.')
            errors = True
        if not errors:
            user.username = username
            user.email = email
            user.bio = bio
            db.session.add(user)
            db.session.commit()
            flash(f'User {username} updated successfully.')
        return redirect(url_for('users.user', id=user.id))
    return render_template('users/edit.html', user=user)

@bp.post('/<int:id>/delete/')
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.index'))
