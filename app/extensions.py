"""Flask extensions for qq2. 

These are instanced in a second file to avoid cyclic imports.
https://stackoverflow.com/a/51739367/3178898
"""
import flask_sqlalchemy
import flask_migrate
import flask_login

db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
manager = flask_login.LoginManager()
