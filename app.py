from flask import Flask, abort, render_template, request, url_for, flash, redirect
from markupsafe import escape # renders URL variable as text to prevent XSS attacks
from datetime import datetime
from forms import CourseForm
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '0b6f5b665fbc26e72c6cffb7de43022196d437ad94b1e8a2' # os.urandom(24).hex()

def get_db_connection():
    conn = sqlite3.connect('qq2.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if not post: 
        abort(404)
    return post

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts, utc_dt=datetime.utcnow())

# messages = [{'title': f'Message {i}', 'content': f'Message {i} content'} for i in range(3)]

# course_list = [{
#     'title': 'Python 101',
#     'description': 'Learn the basics of Python',
#     'price': 55,
#     'available': True,
#     'level': 'Beginner'
# }]

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f'404 at {datetime.utcnow()}: {error}')
    return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return render_template('500.html'), 500

# @app.route('/index-old/', methods=('GET', 'POST'))
# def hello():
#     form = CourseForm()
#     if form.validate_on_submit():
#         course_list.append({
#             'title': form.title.data,
#             'description': form.description.data,
#             'price': form.price.data,
#             'level': form.level.data,
#             'available': form.available.data,
#         })
#         return redirect(url_for('courses'))
#     return render_template('index-old.html', form=form, messages=messages, utc_dt=datetime.utcnow())

@app.route('/about/')
def about():
    return render_template('about.html')

# @app.route('/capitalize/<word>/')
# def capitalize(word):
#     return f'<h1>{escape(word).capitalize()}</h1>'

# @app.route('/add/<int:n1>/<int:n2>/')
# def add(n1, n2):
#     return f'<h1>{n1+n2}</h1>'

# @app.route('/users/<int:user_id>/')
# def greet_user(user_id):
#     users = ['Alice', 'Bob', 'Chuck', 'Diane']
#     try:
#         return f'<h2>Howdy, {users[user_id]}!</h2>'
#     except IndexError:
#         abort(404)

# @app.route('/comments/')
# def comments():
#     comments = [
#         'This is the first comment',
#         'This is the second comment',
#         'This is comment the third (no relation)',
#         "What? You're still here? Go home, the movie's over!",
#     ]
#     return render_template('comments.html', comments=comments)

# @app.route('/messages/<int:idx>/')
# def message(idx):
#     app.logger.info('Building messages list...')
#     _messages = [f'Message {n}' for n in range(10)]
#     try:
#         app.logger.debug(f'Fetching message at index: {idx}')
#         return render_template('message.html', message=_messages[idx])
#     except IndexError:
#         app.logger.error(f'No message found at index: {idx}')
#         abort(404)

# @app.route('/500/')
# def error500():
#     abort(500)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

# @app.route('/courses/')
# def courses():
#     return render_template('courses.html', course_list=course_list)

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts set title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash(f'Post "{post['title']}" deleted.')
    return redirect(url_for('index'))