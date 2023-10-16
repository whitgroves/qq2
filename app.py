from flask import Flask, abort
from markupsafe import escape # renders URL variable as text to prevent XSS attacks

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def hello():
    return '<h1>Hello World</h1>'

@app.route('/about/')
def about():
    return '<h3>A Flask webapp.</h3>'

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
