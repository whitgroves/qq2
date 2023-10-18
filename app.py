from flask import Flask, abort, render_template, request, url_for, flash, redirect
from datetime import datetime
# import sqlite3
import psycopg

app = Flask(__name__)
app.config['SECRET_KEY'] = '0b6f5b665fbc26e72c6cffb7de43022196d437ad94b1e8a2' # os.urandom(24).hex()

def get_db_connection():
    # conn = sqlite3.connect('qq2.db')
    # conn.row_factory = sqlite3.Row
    conn = psycopg.connect(host='localhost', dbname='qq2',
                           user='app', password='qqueue')
    return conn

# def get_post(post_id):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
#     conn.close()
#     if not post: 
#         abort(404)
#     return post

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books, utc_dt=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f'404 at {datetime.utcnow()}: {error}')
    return render_template('404.html'), 404

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = request.form['pages_num']
        review = request.form['review']
        if not title:
            flash('Title required.')
        elif not author:
            flash('Author required.')
        elif not pages_num:
            flash('Number of pages required')
        elif not review:
            flash('Review required')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO books (title, author, pages_num, review)\
                        VALUES (%s, %s, %s, %s)', (title, author, int(pages_num), review))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        # content = request.form['content']
        # if not title:
        #     flash('Title is required!')
        # elif not content:
        #     flash('Content is required!')
        # else:
        #     conn = get_db_connection()
        #     conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        #     conn.commit()
        #     conn.close()
        #     return redirect(url_for('index'))
    return render_template('create.html')

# @app.route('/<int:id>/edit/', methods=('GET', 'POST'))
# def edit(id):
#     post = get_post(id)
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is required!')
#         else:
#             conn = get_db_connection()
#             conn.execute('UPDATE posts set title = ?, content = ? WHERE id = ?', (title, content, id))
#             conn.commit()
#             conn.close()
#         return redirect(url_for('index'))
#     return render_template('edit.html', post=post)

# @app.route('/<int:id>/delete/', methods=('POST',))
# def delete(id):
#     post = get_post(id)
#     conn = get_db_connection()
#     conn.execute('DELETE FROM posts WHERE id = ?', (id,))
#     conn.commit()
#     conn.close()
#     flash(f'Post "{post['title']}" deleted.')
#     return redirect(url_for('index'))