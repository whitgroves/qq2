from pytest import fixture
from app import create_app
from app.extensions import db
from app.models.users import User
from werkzeug.security import generate_password_hash
from config import TestConfig
from flask import Flask
from flask.testing import FlaskClient

@fixture()
def app() -> Flask:
    app = create_app(TestConfig)

    # https://testdriven.io/blog/flask-contexts/#testing-example
    with app.app_context():

        # resource setup
        db.create_all()

        yield app

        # resource cleanup 
        db.drop_all()

@fixture()
def client(app:Flask) -> FlaskClient:
    return app.test_client()
