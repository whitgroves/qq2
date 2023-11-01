"""Test module for qq2. Assumes app/ folder is in the same directory."""
import pytest
import flask
from flask import testing
from werkzeug import security
import app as qq2
from app import models
from app import config as cfg
from app import extensions as ext

# user1_data = dict(email='user1@test.net', username='test1', password='test1')
# user2_data = dict(email='user2@test.net', username='test2', password='test2')

user_data = [{'email':f'user{i}@test.net',
              'username':f'user{i}',
              'password':'test{i}'}
              for i in range(2)]

@pytest.fixture()
def app() -> flask.Flask:
  """Returns a test instance of qq2."""
  qq2_app = qq2.create_app(cfg.TestConfig)

  with qq2_app.app_context(): # setup test records
    test_users = [models.User(email=u['email'],
                  username=u['username'],
                  password=security.generate_password_hash(u['password']))
                  for u in user_data]
    test_post = models.Post(title='Underwater Basket Weaving 101',
                            content='I put on my robe and wizard hat 🧙‍♂️',
                            user=test_users[0])
    test_comments = [models.Comment(content=x,
                                    post=test_post,
                                    user=test_users[0])
                                    for x in ['first', 'second']]
    test_tag = models.Tag(name='depricated')
    test_post.tags.append(test_tag)

    ext.db.session.add_all(test_users)
    ext.db.session.add(test_post)
    ext.db.session.add_all(test_comments)
    ext.db.session.add(test_tag)
    ext.db.session.commit()

    # yielded in app context so downstream fixtures/tests have access to it
    # https://testdriven.io/blog/flask-contexts/#testing-example
    yield qq2_app

@pytest.fixture()
def client(app:flask.Flask) -> testing.FlaskClient: # fixtures, pylint:disable=redefined-outer-name
  """Returns a test client for the test instance."""
  return app.test_client()
