from os.path import join, abspath, dirname
from dotenv import dotenv_values
from os import environ
from secrets import token_hex

local_env = dotenv_values('.env')

class Config:
    SECRET_KEY = local_env.get('SECRET_KEY') or environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = local_env.get('DATABASE_URI') or \
                                environ.get('DATABASE_URI') or \
                                'sqlite:///' + join(abspath(dirname(__file__)), '.data', 'qq2.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class TestConfig(Config):
    TESTING = True
    SECRET_KEY = token_hex(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(abspath(dirname(__file__)), '.data', 'qq2_test.db')
    # WTF_CSRF_ENABLED = False
