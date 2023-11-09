"""Configuration objects for the qq2 app instance.

Config is included as an interface definition. The app will use DefaultConfig 
if no other object is provided, and is setup to use TestConfig under pytest. 

Typical usage:
    import app
    from app import config as cfg
    app_instance = create_app(cfg.TestConfig)
"""
import os
import secrets
import dotenv

local_env = dotenv.dotenv_values('.env')
local_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig: # pylint: disable=too-few-public-methods
    """Interface for qq2 configuration.

    Defines the attributes expected in all configurations when creating app
    instances. When inheriting, make sure to set SECRET_KEY and 
    SQLALCHEMY_DATABASE_URI.

    Attributes:
        SECRET_KEY: The app's secret key. Used mainly to generate CSRF tokens.
        SQLALCHEMY_DATABASE_URI: Connection string for the app's database.
        SQLALCHEMY_TRACK_MODIFICATIONS: Whether to track db modifications.
        TESTING: Whether the app is in testing mode.
    """
    SECRET_KEY = ''
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class DefaultConfig(BaseConfig): # pylint: disable=too-few-public-methods
    """Default config for the app.
    
    Attempts to pull SECRET_KEY from a local .env file, or the environment
    variables if no file is provided. SQLALCHEMY_DATABASE_URI follows the same
    pattern, except it will create a SQLite database at ./.data/qq2.db by
    default if no connection string is provided.
    """
    SECRET_KEY = local_env.get('SECRET_KEY') or os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = local_env.get('DATABASE_URI') or \
                             os.environ.get('DATABASE_URI') or \
                'sqlite:///' + os.path.join(local_dir,'.data','qq2.db')

class TestConfig(BaseConfig): # pylint: disable=too-few-public-methods
    """Testing config for the app.

    SECRET_KEY is randomly generated for each instance, and 
    SQLALCHEMY_DATABASE_URI always creates a SQLite test database at 
    ./.testdata/qq2_test.db
    """
    TESTING = True
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(local_dir,'.testdata', 'qq2_test.db')
    # WTF_CSRF_ENABLED = False
