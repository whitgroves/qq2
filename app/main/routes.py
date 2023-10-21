from flask import render_template
from app.main import bp

from datetime import datetime

@bp.route('/')
def index():
    return render_template('index.html', utc_dt=datetime.utcnow())