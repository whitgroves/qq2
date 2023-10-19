from flask import Flask, abort, render_template, request, url_for, flash, redirect
from datetime import datetime
# import psycopg
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = '0b6f5b665fbc26e72c6cffb7de43022196d437ad94b1e8a2' # os.urandom(24).hex()

client = MongoClient('localhost', 27017)
db = client.qq2
tasks = db.tasks

# def get_db_connection():
#     conn = psycopg.connect(host='localhost', dbname='qq2',
#                            user='app', password='qqueue')
#     return conn

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        description = request.form['description']
        importance = request.form['importance']
        tasks.insert_one({'description': description, 'importance': importance})
        return redirect(url_for('index'))
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM books')
#     books = cur.fetchall()
#     cur.close()
#     conn.close()
    all_tasks = tasks.find()
    return render_template('index.html', tasks=all_tasks, utc_dt=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f'404 at {datetime.utcnow()}: {error}')
    return render_template('404.html'), 404

@app.route('/about/')
def about():
    return render_template('about.html')

# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         author = request.form['author']
#         pages_num = request.form['pages_num']
#         review = request.form['review']
#         if not title:
#             flash('Title required.')
#         elif not author:
#             flash('Author required.')
#         elif not pages_num:
#             flash('Number of pages required')
#         elif not review:
#             flash('Review required')
#         else:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute('INSERT INTO books (title, author, pages_num, review)\
#                         VALUES (%s, %s, %s, %s)', (title, author, int(pages_num), review))
#             conn.commit()
#             cur.close()
#             conn.close()
#             return redirect(url_for('index'))
#     return render_template('create.html')

@app.post('/<id>/delete/')
def delete(id):
    tasks.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))
