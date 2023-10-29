from flask import g # global app context for CSRF token, see test_auth.py
from flask.testing import FlaskClient
from .conftest import user_data

user0 = user_data[0]
user1 = user_data[1]

def test_index(client:FlaskClient) -> None:
    # Page loads with all info
    response = client.get('/users/')
    assert all(u['username'] in response.text for u in user_data)

def test_user(client:FlaskClient) -> None:
    # Page loads with all info
    response = client.get('/users/1')
    assert user_data[0]['email'] in response.text

def test_edit(client:FlaskClient) -> None:
    # Setup - login
    client.get('/login') # generates CSRF token, but we also need to login to edit
    login_data = dict(csrf_token=g.csrf_token, user_email=user0['email'], password=user0['password'])
    client.post('/login', data=login_data)

    # Page loads with all info (when signed in)
    response_get_valid = client.get('/users/1/edit')
    assert all(x in response_get_valid.text for x in ['Email',
                                                      'Username',
                                                      'Bio',
                                                      'Update',
                                                      'Delete'])
    
    # User data is updated successfully
    bio = 'Not turtle-y enough for the turtle club.'
    update_data_valid = dict(csrf_token=g.csrf_token, bio=bio, **user0)
    response_post_valid = client.post('/users/1/edit', data=update_data_valid, follow_redirects=True)
    assert response_post_valid.status_code == 200
    assert response_post_valid.request.path == '/users/1/edit'
    response_post_valid_confirm = client.get('/users/1')
    assert bio in response_post_valid_confirm.text

    # Cannot update without CSRF token
    update_data_no_token = dict(bio="That boy ain't right.", **user0)
    response_post_no_token = client.post('/users/1/edit', data=update_data_no_token)
    assert response_post_no_token.status_code == 400

    # Cannot update email to existing address on another account
    update_data_duplicate_email = dict(csrf_token=g.csrf_token, email=user1['email'])
    response_duplicate_email = client.post('/users/1/edit', data=update_data_duplicate_email)
    assert response_duplicate_email.status_code == 400

    # Cannot update another account
    update_data_wrong_account = dict(csrf_token=g.csrf_token, **user1)
    response_wrong_account = client.post('/users/2/edit', data=update_data_wrong_account)
    assert response_wrong_account.status_code == 403

    # Cannot update when logged out; redirects to login
    client.get('/logout')
    response_no_login = client.post('/users/1/edit', data=update_data_valid)
    assert response_no_login.status_code == 302
    assert response_no_login.location[:6] == '/login' # some params are appended
