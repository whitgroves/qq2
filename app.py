from flask import Flask, abort, render_template, request, url_for, flash, redirect
from datetime import datetime
from os.path import abspath, dirname, join
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SECRET_KEY'] = '0b6f5b665fbc26e72c6cffb7de43022196d437ad94b1e8a2' # os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(abspath(dirname(__file__)), 'qq2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(80), nullable=False, unique=True)
#     age = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) # func.now() renders as CURRENT_TIMESTAMP at table creation
#     bio = db.Column(db.Text)
#     # posts = db.relationship('Post', backref='user')
#     # comments = db.relationship('Comment', backref='user')

#     def __repr__(self):
#         return f'<User {self.username}>'
# #endclass

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comments = db.relationship('Comment', backref='post')
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'
#endclass

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Tag "{self.name}">'
#endclass

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f'<Comment {self.id}: {self.content[:20]}>'
#endclass

@app.route('/')
def index():
    # users = User.query.all()
    posts = Post.query.all()
    return render_template('index.html', posts=posts, utc_dt=datetime.utcnow())

@app.route('/post/<int:id>/', methods=('GET', 'POST'))
def post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        content = request.form['content']
        if len(content) == 0:
            flash('Comment cannot be blank')
        else:
            comment = Comment(content=content, post=post)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('post', id=post.id))
    return render_template('post.html', post=post)

@app.route('/comments/')
def comments():
    comments = Comment.query.order_by(Comment.id.desc()).all()
    return render_template('comments.html', comments=comments)

@app.post('/comments/<int:id>/delete/')
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('post', id=post_id))

@app.route('/tag/<name>/')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)

# @app.route('/user/<int:id>/')
# def user(id):
#     user = User.query.get_or_404(id)
#     return render_template('user.html', user=user)

# def handle_user_update(form, user=None) -> tuple[bool, str]:
#     username = form['username']
#     email = form['email']
#     age = form['age']
#     bio = form['bio']
#     if any(len(x) == 0 for x in [username, email]):
#         return False, 'Username and email required'
#     try:
#         if user is not None:
#             user.username = username
#             user.email = email
#             user.age = age
#             user.bio = bio
#         else:
#             if len(User.query.filter_by(email=email).all()) > 0:
#                 return False, 'Email must be unique'
#             user = User(username=username, email=email, age=age, bio=bio)
#         db.session.add(user)
#         db.session.commit()
#         return True, f'Successfully added user {username}'
#     except Exception as e:
#         app.logger.error(f'Error while writing to database: {e}')
#         return False, 'Something went wrong'

# @app.route('/user/create/', methods=('GET', 'POST'))
# def create_user():
#     if request.method == 'POST':
#         success, msg = handle_user_update(request.form)
#         if success:
#             return redirect(url_for('index'))
#         else: 
#             flash(msg)
#             return render_template('create.html', user=request.form)
#     return render_template('create.html')

# @app.route('/user/<int:id>/edit/', methods=('GET', 'POST'))
# def edit_user(id):
#     user = User.query.get_or_404(id)
#     if request.method == 'POST':
#         success, msg = handle_user_update(request.form, user)
#         if success:
#             return redirect(url_for('index'))
#         else: 
#             flash(msg)
#             return render_template('edit.html', user=user)
#     return render_template('edit.html', user=user)

# @app.post('/user/<int:id>/delete/')
# def delete_user(id):
#     user = User.query.get_or_404(id)
#     db.session.delete(user)
#     db.session.commit()
#     return redirect(url_for('index'))

@app.route('/about/')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f'404 at {datetime.utcnow()}: {error}')
    return render_template('404.html'), 404
