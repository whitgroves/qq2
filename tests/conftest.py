"""Test module for qq2. Assumes app/ is in the same parent directory."""
import pytest
import flask
import flask.testing
import werkzeug.security as ws
import app as qq2
from app import models
from app import config as cfg
from app import extensions as ext

# user1_data = dict(email='user1@test.net', username='test1', password='test1')
# user2_data = dict(email='user2@test.net', username='test2', password='test2')

user_data = [{'email':f'user{i}@test.net',
              'username':f'user{i}',
              'password':f'test{i}'} for i in range(2)]

post_data = [{'title': f'Underwater Basket Weaving {i+1}01',
              'content': f'Step {i+1}: I put on my robe and wizard hat 🧙‍♂️'} 
              for i in range(2)]

@pytest.fixture()
def app() -> flask.Flask:
    """Creates an instance of the qq2 app.
    
    Each instance is seeded with test records and returned within qq2's app
    context for ease of writing tests.
    """
    qq2_app = qq2.create_app(cfg.TestConfig)

    with qq2_app.app_context(): # setup test records
        test_users = [models.User(email=u['email'],
                                  username=u['username'],
                                  password= \
                                    ws.generate_password_hash(u['password']))
                                  for u in user_data]
        test_posts = [models.Post(title=t['title'],
                                  content=t['content'],
                                  user=test_users[0])
                                  for t in post_data]
        test_comments = [models.Comment(content=x,
                                        post=test_posts[0],
                                        user=test_users[0])
                                        for x in ['first', 'second']]
        test_tag = models.Tag(name='depricated')
        test_posts[0].tags.append(test_tag)

        ext.db.session.add_all(test_users)
        ext.db.session.add_all(test_posts)
        ext.db.session.add_all(test_comments)
        ext.db.session.add(test_tag)
        ext.db.session.commit()

        # yielded in app context so downstream fixtures/tests have access to it
        # https://testdriven.io/blog/flask-contexts/#testing-example
        yield qq2_app

@pytest.fixture()
def client(app:flask.Flask) -> flask.testing.FlaskClient: # fixtures, pylint:disable=redefined-outer-name
    return app.test_client()
