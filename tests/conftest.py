from pytest import fixture
from app import create_app
from app.extensions import db
from app.models.users import User
from app.models.posts import Post, Comment, Tag
from werkzeug.security import generate_password_hash
from config import TestConfig
from flask import Flask
from flask.testing import FlaskClient

# user1_data = dict(email='user1@test.net', username='test1', password='test1')
# user2_data = dict(email='user2@test.net', username='test2', password='test2')

user_data = [dict(email=f'user{i}@test.net', username=f'user{i}', password=f'test{i}') for i in range(2)]

@fixture()
def app() -> Flask:
    app = create_app(TestConfig)

    # https://testdriven.io/blog/flask-contexts/#testing-example
    with app.app_context():

        # resource setup
        db.create_all()
        test_users = [User(email=u['email'], username=u['username'], password=generate_password_hash(u['password'])) for u in user_data]
        test_post = Post(title='Underwater Basket Weaving 101', content='I put on my robe and wizard hat 🧙‍♂️', user=test_users[0])
        test_comments = [Comment(content=x, post=test_post, user=test_users[0]) for x in ['first', 'second']]
        test_tag = Tag(name='depricated')
        test_post.tags.append(test_tag)
        db.session.add_all(test_users)
        db.session.add(test_post)
        db.session.add_all(test_comments)
        db.session.add(test_tag)
        db.session.commit()

        yield app

        # resource cleanup 
        db.drop_all()

@fixture()
def client(app:Flask) -> FlaskClient:
    return app.test_client()
