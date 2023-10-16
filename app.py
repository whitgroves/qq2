from flask import Flask, abort, render_template
from markupsafe import escape # renders URL variable as text to prevent XSS attacks
import datetime

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/')
@app.route('/index/')
def hello():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/capitalize/<word>/')
def capitalize(word):
    return f'<h1>{escape(word).capitalize()}</h1>'

@app.route('/add/<int:n1>/<int:n2>/')
def add(n1, n2):
    return f'<h1>{n1+n2}</h1>'

@app.route('/users/<int:user_id>/')
def greet_user(user_id):
    users = ['Alice', 'Bob', 'Chuck', 'Diane']
    try:
        return f'<h2>Howdy, {users[user_id]}!</h2>'
    except IndexError:
        abort(404)

@app.route('/comments/')
def comments():
    comments = [
        'This is the first comment',
        'This is the second comment',
        'This is comment the third (no relation)',
        "What? You're still here? Go home, the movie's over!",
    ]
    return render_template('comments.html', comments=comments)

@app.route('/messages/<int:idx>/')
def message(idx):
    app.logger.info('Building messages list...')
    messages = [f'Message {n}' for n in range(10)]
    try:
        app.logger.debug(f'Fetching message at index: {idx}')
        return render_template('message.html', message=messages[idx])
    except IndexError:
        app.logger.error(f'No message found at index: {idx}')
        abort(404)

@app.route('/500/')
def error500():
    abort(500)