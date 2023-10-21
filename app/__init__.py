from flask import Flask
from config import Config
from app.extensions import db

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # init extensions (e.g. sqlalchemy)
    db.init_app(app)

    # register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask App Factory Pattern</h1>'
    
    return app