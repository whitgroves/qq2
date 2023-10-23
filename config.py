from os.path import join, abspath, dirname
from dotenv import dotenv_values
from os import environ

local_env = dotenv_values('.env')

class Config:
    SECRET_KEY = local_env.get('SECRET_KEY') or environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = \
        local_env.get('DATABASE_URI') or 'sqlite:///' + join(abspath(dirname(__file__)), 'qq2.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
