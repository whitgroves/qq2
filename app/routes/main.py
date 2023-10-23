from flask import Blueprint, render_template
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index() -> str:
    return render_template('index.html', utc_dt=datetime.utcnow())

@bp.route('/about')
def about() -> str:
    links = [
        'https://www.digitalocean.com/community/tutorial-series/how-to-create-web-sites-with-flask',
        'https://getbootstrap.com/docs/5.3/getting-started/introduction/',
        'https://flask.palletsprojects.com/en/3.0.x/cli/',
        'https://www.codium.ai/blog/flask-sqlalchemy-tutorial/',
        'https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login',
        'https://stackoverflow.com/questions/77215107/importerror-cannot-import-name-url-decode-from-werkzeug-urls',
    ]
    return render_template('about.html', links=links)