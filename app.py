from flask import Flask, abort, render_template, request, url_for, flash, redirect
from datetime import datetime
# from pymongo import MongoClient
# from bson import ObjectId
from os.path import abspath, dirname, join
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SECRET_KEY'] = '0b6f5b665fbc26e72c6cffb7de43022196d437ad94b1e8a2' # os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(abspath(dirname(__file__)), 'qq2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) # func.now() renders as CURRENT_TIMESTAMP at table creation
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.username}>'
#endclass

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users, utc_dt=datetime.utcnow())

@app.route('/user/<int:id>/')
def user(id):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)

def handle_user_update(form, user=None) -> tuple[bool, str]:
    username = form['username']
    email = form['email']
    age = form['age']
    bio = form['bio']
    if any(len(x) == 0 for x in [username, email]):
        return False, 'Username and email required'
    try:
        if user is not None:
            user.username = username
            user.email = email
            user.age = age
            user.bio = bio
        else:
            if len(User.query.filter_by(email=email).all()) > 0:
                return False, 'Email must be unique'
            user = User(username=username, email=email, age=age, bio=bio)
        db.session.add(user)
        db.session.commit()
        return True, f'Successfully added user {username}'
    except Exception as e:
        app.logger.error(f'Error while writing to database: {e}')
        return False, 'Something went wrong'

@app.route('/user/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        success, msg = handle_user_update(request.form)
        if success:
            return redirect(url_for('index'))
        else: 
            flash(msg)
            return render_template('create.html', user=request.form)
    return render_template('create.html')

@app.route('/user/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        success, msg = handle_user_update(request.form, user)
        if success:
            return redirect(url_for('index'))
        else: 
            flash(msg)
            return render_template('edit.html', user=user)
    return render_template('edit.html', user=user)

@app.post('/user/<int:id>/delete/')
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about/')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f'404 at {datetime.utcnow()}: {error}')
    return render_template('404.html'), 404
