from flask import g # global app context
from flask.testing import FlaskClient

# To test Flask-WTForms without setting WTF_CSRF_ENABLED=False, we do a little wizardry based on
# https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72?permalink_comment_id=4556252#gistcomment-4556252
# Essentially a GET request will generate a valid CSRF token, then we can pull it from the global app context

test_user = dict(email='user@email.com', password='test', username='test')

def test_register(client:FlaskClient) -> None:
    
    # All fields present on form
    response_get = client.get('/register') # creates CSRF token - do NOT move
    assert all(x in response_get.text for x in ['Email', 'Username', 'Password'])

    # Registration denied without CSRF token
    response_post_no_csrf = client.post('/register', data=test_user)
    assert response_post_no_csrf.status_code == 400
    
    # Registration accepted with CSRF token and redirects to login on success
    post_data_csrf = dict(csrf_token=g.csrf_token, **test_user)
    response_post_csrf = client.post('/register', data=post_data_csrf, follow_redirects=True)
    assert response_post_csrf.status_code == 200
    assert len(response_post_csrf.history) == 1
    assert response_post_csrf.request.path == '/login'

    # Duplicate email is rejected, even with token
    response_post_dupe = client.post('/register', data=post_data_csrf)
    assert response_post_dupe.status_code == 400

def test_login(client:FlaskClient) -> None:

    # Setup - register test_user
    client.get('/register') # creates CSRF token - do NOT move
    client.post('/register', data=dict(csrf_token=g.csrf_token, **test_user))

    # All fields present on form
    response_get = client.get('/login') # does not create a new CSRF token
    assert all(x in response_get.text for x in ['Username or Email', 'Password'])

    # User can login with email and is redirected to homepage
    post_data_email = dict(csrf_token=g.csrf_token, user_email=test_user['email'], password=test_user['password'])
    response_post_email = client.post('/login', data=post_data_email, follow_redirects=True)
    assert response_post_email.status_code == 200
    assert len(response_post_email.history) == 1
    assert response_post_email.request.path == '/'

    # User can login with username and is redirected to homepage
    post_data_username = dict(csrf_token=g.csrf_token, user_email=test_user['username'], password=test_user['password'])
    response_post_username = client.post('/login', data=post_data_username, follow_redirects=True)
    assert response_post_username.status_code == 200
    assert len(response_post_username.history) == 1
    assert response_post_username.request.path == '/'

    # Login denied without CSRF token, even with valid credentials
    post_data_no_csrf = dict(user_email=test_user['email'], password=test_user['password'])
    response_post_no_csrf = client.post('/login', data=post_data_no_csrf)
    assert response_post_no_csrf.status_code == 400

    # Login denied with invalid password, even with CSRF token
    post_data_bad_password = dict(csrf_token=g.csrf_token, user_email=test_user['email'], password='wrong')
    response_post_bad_password = client.post('/login', data=post_data_bad_password)
    assert response_post_bad_password.status_code == 400

    # Login denied with non-registered email
    post_data_bad_email = dict(csrf_token=g.csrf_token, user_email='user@wrong.com', password=test_user['password'])
    response_post_bad_email = client.post('/login', data=post_data_bad_email)
    assert response_post_bad_email.status_code == 400

    # Login denied with non-registered username
    post_data_bad_username = dict(csrf_token=g.csrf_token, user_email='not_a_user', password=test_user['password'])
    response_post_bad_username = client.post('/login', data=post_data_bad_username)
    assert response_post_bad_username.status_code == 400

def test_logout(client:FlaskClient) -> None:

    # Setup - register test_user and login
    client.get('/register') # creates CSRF token - do NOT move
    client.post('/register', data=dict(csrf_token=g.csrf_token, **test_user))
    login_data = dict(csrf_token=g.csrf_token, user_email=test_user['email'], password=test_user['password'])
    client.post('/login', data=login_data)

    # Logout redirects to the homepage
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == '/'