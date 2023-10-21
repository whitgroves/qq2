from os.path import join, abspath, dirname
from dotenv import dotenv_values

local_env = dotenv_values('.env')

class Config:
    SECRET_KEY = local_env['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = \
        local_env['DATABASE_URI'] if 'DATABASE_URI' in local_env else \
        'sqlite:///' + join(abspath(dirname(__file__)), 'qq2.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
