from flask import Flask
from config import Config
from app.extensions import db, migrate, manager

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # init extensions (e.g. database)
    db.init_app(app)
    migrate.init_app(app, db)
    manager.init_app(app)

    # login management
    manager.login_view = 'auth.login'
    from app.models.users import User
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
    
    return app