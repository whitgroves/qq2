from flask import render_template
from app.users import bp
from app.models.user import User

@bp.route('/')
def index():
    users = User.query.filter_by(active=True).all()
    return render_template('users/index.html', users=users)