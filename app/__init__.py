""" A Flask microservice to practice web development.

The current version supports basic accounts - users can register with an email/
password and login to update or delete their profile.

Typical usage (from CLI):
    $ flask run --port=80
"""
import os
import logging
import flask
import flask.logging
import sqlalchemy as alq
from app import config as cfg
from app import extensions as ext

# log styling
flask.logging.default_handler.setFormatter(
    logging.Formatter('qq2 [{levelname}]: {message}', style='{'))

def create_app(config:cfg.BaseConfig=cfg.DefaultConfig) -> flask.Flask:
    """Creates an instance of qq2 using the App Factory pattern.

    Creates a flask.Flask instance based on the settings defined in <config>.

    Args:
        config: A Config object. Must include these properties SECRET_KEY, 
            SQLALCHEMY_DATABASE_URI, and TESTING.

    Returns:
        A flask.Flask instance.
    """
    app = flask.Flask(__name__)

    # load config
    app.config.from_object(config)
    if app.testing:
        app.logger.info('App configured for testing mode.')

    # init extensions
    ext.db.init_app(app)
    ext.migrate.init_app(app, ext.db)
    ext.manager.init_app(app)

    # internal imports - done this way to avoid circular reference
    from app import models # pylint: disable=import-outside-toplevel
    from app.routes.main import bp as main_routes   # pylint: disable=import-outside-toplevel
    from app.routes.auth import bp as auth_routes   # pylint: disable=import-outside-toplevel
    from app.routes.users import bp as user_routes  # pylint: disable=import-outside-toplevel
    from app.routes.posts import bp as post_routes  # pylint: disable=import-outside-toplevel

    # login management
    ext.manager.login_view = 'auth.login'
    @ext.manager.user_loader
    def load_user(_id):
        return models.User.query.get(int(_id))

    # register blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(user_routes, url_prefix='/users')
    app.register_blueprint(post_routes, url_prefix='/posts')

    # init db - if db is missing or missing tables, setup a new one
    init_db(app, config)

    return app

def init_db(app:flask.Flask, config:cfg.BaseConfig) -> bool:
    """Initializes the database.

    Attempts to find the database at <config> and create one if it doesn't 
    exist (SQLite only), or rebuild the database if any tables are missing. 

    Args:
        app: The app instance to setup the database for.

    Returns:
        True if the database was rebuilt, False otherwise.
    """
    # internal import - done this way to avoid circular reference
    from app import models # pylint: disable=import-outside-toplevel

    rebuild = config.TESTING # always rebuild on test

    if 'sqlite:///' in config.SQLALCHEMY_DATABASE_URI:
        db_path = os.path.dirname(config.SQLALCHEMY_DATABASE_URI.split('sqlite:///')[-1])
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            rebuild = True

    with app.app_context(): # db read/writes require app context

        db_models = [models.User, models.Post, models.Comment, models.Tag]
        inspector = alq.inspect(ext.db.engine)
        if not all(inspector.has_table(x.__tablename__) for x in db_models):
            app.logger.warning('Tables missing in database. Rebuilding...')
            rebuild = True

        if rebuild:
            app.logger.info('Initializing database...')
            ext.db.drop_all()
            ext.db.create_all()

    app.logger.info('Database ready.')

    return rebuild
