"""Test for the post routes of qq2.

This test relies on using flask's global app context to generate/fetch CSRF
tokens for protected forms. See test_auth.py for full explanation.
"""
import flask
from flask import testing
from .conftest import user_data

user0 = user_data[0]
user1 = user_data[1]

def test_index(client:testing.FlaskClient) -> None:
    """Tests that the post list displays correctly."""
    # Page loads with all info
    response = client.get('/posts/')
    assert response.status_code == 200
    assert all(x in response.text for x in ['Underwater Basket Weaving 101',
                                            'I put on my robe and wizard hat 🧙‍♂️',
                                            '2 Comments', # update if more comments added to test db
                                            'depricated'])

def test_post(client:testing.FlaskClient) -> None:
    """Tests behavior for viewing individual posts."""
    # Page loads with all info
    response = client.get('/posts/1')
    assert response.status_code == 200
    assert all(x in response.text for x in ['Underwater Basket Weaving 101',
                                            'I put on my robe and wizard hat 🧙‍♂️',
                                            'first',
                                            'second',
                                            'depricated'])

    # Redirect to index on bad post id
    response = client.get('/posts/2', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/posts/'

def test_tags(client:testing.FlaskClient) -> None:
    """Tests that all tags are in the list."""
    # Page loads with all info
    response = client.get('/posts/tags/')
    assert response.status_code == 200
    assert all(x in response.text for x in ['depricated'])

def test_tag(client:testing.FlaskClient) -> None:
    """Test that a particular tag shows all tagged posts."""
    # Page loads with all info
    response = client.get('/posts/tags/depricated')
    assert response.status_code == 200
    assert all(x in response.text for x in ['Underwater Basket Weaving 101',
                                            'I put on my robe and wizard hat 🧙‍♂️',
                                            '2 Comments', # update if more comments added to test db
                                            'depricated'])

def test_comments(client:testing.FlaskClient) -> None:
    """Tests all comments are in the list."""
    # Page loads with all info
    response = client.get('/posts/comments/')
    assert response.status_code == 200
    assert all(x in response.text for x in [user0['username'], 'first', 'second'])

def test_add_comment(client:testing.FlaskClient) -> None:
    """Tests the ability for users to add comments.
    
    Note that the initial GET request to /login is required to generate the
    CSRF token and it must be included for successful requests.
    """
    # Setup - login
    client.get('/login') # creates CSRF token - do NOT move
    login_data = {'csrf_token': flask.g.csrf_token,
                  'user_email': user0['email'],
                  'password': user0['password']}
    client.post('/login', data=login_data) #pylint: disable=duplicate-code

    # Comment is added successfully
    content_valid = {'csrf_token': flask.g.csrf_token, 'content': 'third'}
    response_valid = client.post('/posts/1/comments/add/',
                                 data=content_valid,
                                 follow_redirects=True)
    assert response_valid.status_code == 200
    assert response_valid.request.path == '/posts/1'
    assert content_valid['content'] in response_valid.text

    # Can't add empty comment (ignore redirect for post result)
    content_empty = {'csrf_token': flask.g.csrf_token}
    response_empty = client.post('/posts/1/comments/add/', data=content_empty)
    assert response_empty.status_code == 400

    # Can't add comment to nonexistent post
    response_no_post = client.post('/posts/2/comments/add/', data=content_valid)
    assert response_no_post.status_code == 404

    # Can't add comment without token
    response_no_token = client.post('/posts/1/comments/add/', data={'content':'minato'})
    assert response_no_token.status_code == 400

    # Can't comment while logged out; redirects to login
    client.get('/logout') # do NOT move
    content_no_login = {'csrf_token': flask.g.csrf_token, 'content': 'fif'}
    response_no_login = client.post('/posts/1/comments/add/', data=content_no_login)
    assert response_no_login.status_code == 302
    assert response_no_login.location[:6] == '/login' # some params are appended

    # confirm comment was not pushed despite redirect
    all_comments = client.get('/posts/comments/')
    assert content_no_login['content'] not in all_comments.text

def test_delete_comment(client:testing.FlaskClient) -> None:
    """Tests the ability for users to delete comments.
    
    Note that the initial GET request to /login is required to generate the
    CSRF token and it must be included for successful requests.
    """
    # Setup - login
    client.get('/login') # creates CSRF token - do NOT move
    login_data = {'csrf_token': flask.g.csrf_token,
                  'user_email': user0['email'],
                  'password': user0['password']}
    client.post('/login', data=login_data)

    # Comment is deleted successfully
    response_valid = client.post('/posts/comments/1/delete/', follow_redirects=True)
    assert response_valid.status_code == 200
    assert response_valid.request.path == '/posts/1'
    assert 'first' not in response_valid.text

    # Can't delete same comment twice
    response_double_delete = client.post('/posts/comments/1/delete/')
    assert response_double_delete.status_code == 404

    # Can't delete nonexistent comment
    response_nonexistent = client.post('/posts/comments/3/delete/')
    assert response_nonexistent.status_code == 404

    # Can't delete comment while logged out; redirects to login
    client.get('/logout')
    response_no_login = client.post('/posts/comments/2/delete/')
    assert response_no_login.status_code == 302
    assert response_no_login.location[:6] == '/login' # some params are appended
    all_comments = client.get('/posts/comments/')
    assert 'second' in all_comments.text # confirm comment was not deleted despite redirect

    # Can't delete comment while logged in as another user
    login_data = {'csrf_token': flask.g.csrf_token,
                  'user_email': user1['email'],
                  'password': user1['password']}
    client.post('/login', data=login_data)
    response_wrong_user = client.post('/posts/comments/2/delete/')
    assert response_wrong_user.status_code == 403
