"""The main set of routes for qq2."""
import datetime
import flask

bp = flask.Blueprint('main', __name__)

@bp.route('/')
def index() -> flask.Response:
  """Returns the homepage."""
  return flask.render_template('index.html',
                               utc_dt=datetime.datetime.now(datetime.UTC))

@bp.route('/about')
def about() -> flask.Response:
  """Returns the about page."""
  return flask.render_template('about.html')
