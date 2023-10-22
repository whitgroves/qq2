from flask import Flask
from config import Config
from app.extensions import db, migrate

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # init extensions (e.g. database)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    
    return app