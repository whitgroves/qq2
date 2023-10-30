from flask import Flask
from flask.logging import default_handler
from logging import Formatter
from config import Config
from app.extensions import db, migrate, manager
from app.models.users import User
from app.models.posts import Post, Comment, Tag # included for db init, see EOF
from os.path import exists, dirname
from os import makedirs

default_handler.setFormatter(Formatter('qq2 [{levelname}]: {message}', style='{'))

def create_app(config=Config) -> Flask:
    app = Flask(__name__)

    # load config
    app.config.from_object(config)
    if app.testing:
        app.logger.info('App configured for testing mode.')

    # init extensions 
    db.init_app(app)
    migrate.init_app(app, db)
    manager.init_app(app)

    # login management
    manager.login_view = 'auth.login'
    @manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # register blueprints
    from app.routes.main import bp as main_routes
    app.register_blueprint(main_routes)

    from app.routes.auth import bp as auth_routes
    app.register_blueprint(auth_routes)

    from app.routes.users import bp as user_routes
    app.register_blueprint(user_routes, url_prefix='/users')

    from app.routes.posts import bp as post_routes
    app.register_blueprint(post_routes, url_prefix='/posts')
    
    # init db - must import data models for SQLAlchemy first to build out all tables
    db_file = config.SQLALCHEMY_DATABASE_URI.split('sqlite:///')[-1]
    db_path = dirname(db_file)
    if not exists(db_path): makedirs(db_path)
    if config.TESTING or not exists(db_file):
        app.logger.info('Initializing database...')
        with app.app_context():
            db.drop_all()
            db.create_all()
    app.logger.info('Database ready.')
    app.logger.debug(f'Database URI: {config.SQLALCHEMY_DATABASE_URI}')
    
    return app
