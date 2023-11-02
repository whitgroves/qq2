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
    # Page loads with all info
    response = client.get('/posts/')
    assert response.status_code == 200
    assert all(x in response.text
               for x in ['Underwater Basket Weaving 101',
                         'I put on my robe and wizard hat 🧙‍♂️',
                         '2 Comments', # update if more added to test db
                         'depricated'])

def test_post(client:testing.FlaskClient) -> None:
    # Page loads with all info
    response = client.get('/posts/1')
    assert response.status_code == 200
    assert all(x in response.text
               for x in ['Underwater Basket Weaving 101',
                         'I put on my robe and wizard hat 🧙‍♂️',
                         'first',
                         'second',
                         'depricated'])

    # Redirect to index on bad post id
    response = client.get('/posts/2', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/posts/'

def test_new_post(client:testing.FlaskClient) -> None:
    # Setup - login
    client.get('/login') # creates CSRF token - do NOT move
    login_data = {'csrf_token': flask.g.csrf_token,
                  'user_email': user0['email'],
                  'password': user0['password']}
    client.post('/login', data=login_data) #pylint: disable=duplicate-code

     # Post is added successfully
    content_valid = {'csrf_token': flask.g.csrf_token,
                     'title': 'post #2',
                     'content': 'the second post'}
    response_valid = client.post('/posts/new',
                                 data=content_valid,
                                 follow_redirects=True)
    assert response_valid.status_code == 200
    assert response_valid.request.path == '/posts/2'
    assert all(content_valid[x] in response_valid.text
               for x in ['title', 'content'])

    # Can't add post without title (ignore redirect for post result)
    no_title = {'csrf_token': flask.g.csrf_token, 'content': 'fluff'}
    response_no_title = client.post('/posts/new', data=no_title)
    assert response_no_title.status_code == 400

    # Can't add post without content (ignore redirect for post result)
    no_content = {'csrf_token': flask.g.csrf_token, 'title': 'stuff'}
    response_no_content = client.post('/posts/new', data=no_content)
    assert response_no_content.status_code == 400

    # Can't add post without token
    response_no_token = client.post('/posts/new', data={'title': 'nope',
                                                        'content':'negative'})
    assert response_no_token.status_code == 400

    # Can't post while logged out; redirects to login
    client.get('/logout') # do NOT move
    content_no_login = {'csrf_token': flask.g.csrf_token,
                        'title': 'the show',
                        'content': 'fif'}
    response_no_login = client.post('/posts/new', data=content_no_login)
    assert response_no_login.status_code == 302
    assert response_no_login.location[:6] == '/login' # some params are appended

    # confirm post was not pushed despite redirect
    all_posts = client.get('/posts/')
    assert all(x not in all_posts.text for x in ['the show', 'fif'])

def test_edit_post(client:testing.FlaskClient) -> None:
    # Setup - login
    client.get('/login') # creates CSRF token - do NOT move
    login_data = {'csrf_token': flask.g.csrf_token,
                  'user_email': user0['email'],
                  'password': user0['password']}
    client.post('/login', data=login_data) #pylint: disable=duplicate-code

     # Post is edited successfully - user 0 owns all posts
    data_valid = {'csrf_token': flask.g.csrf_token,
                  'title': 'updated title',
                  'content': 'updated content'}
    response_valid = client.post('/posts/1/edit',
                                 data=data_valid,
                                 follow_redirects=True)
    assert response_valid.status_code == 200
    assert response_valid.request.path == '/posts/1'
    assert all(x in response_valid.text
               for x in ['updated title', 'updated content'])

    # Can update with no title - will default to previous title
    no_title = {'csrf_token': flask.g.csrf_token, 'content': 'fluff'}
    response_no_title = client.post('/posts/1/edit',
                                    data=no_title,
                                    follow_redirects=True)
    assert response_valid.status_code == 200
    assert response_valid.request.path == '/posts/1'
    assert 'updated content' not in response_no_title.text # from previous edit
    assert all(x in response_no_title.text for x in ['fluff', 'updated title'])

    # Can update with no content - will default to previous content
    no_content = {'csrf_token': flask.g.csrf_token, 'title': 'stuff'}
    response_no_content = client.post('/posts/1/edit',
                                      data=no_content,
                                      follow_redirects=True)
    assert response_valid.status_code == 200
    assert response_valid.request.path == '/posts/1'
    assert 'updated title' not in response_no_content.text # from previous edit
    assert all(x in response_no_content.text for x in ['fluff', 'stuff'])

    # Can't edit without token
    response_no_token = client.post('/posts/1/edit', data={'title': 'nope',
                                                           'content':'iie'})
    assert response_no_token.status_code == 400

    # Can't edit post while logged out; redirects to login
    client.get('/logout') # do NOT move
    post_no_login = {'csrf_token': flask.g.csrf_token,
                     'title': '24',
                     'content': '25'}
    response_no_login = client.post('/posts/1/edit', data=post_no_login)
    assert response_no_login.status_code == 302
    assert response_no_login.location[:6] == '/login' # some params are appended

    # confirm post was not edited despite redirect
    all_comments = client.get('/posts/')
    assert all(x not in all_comments.text for x in ['24', '25'])

    # Can't edit comment while logged in as another user
    login_data = {'csrf_token': flask.g.csrf_token,
                                'user_email': user1['email'],
                                'password': user1['password']}
    client.post('/login', data=login_data)
    response_wrong_user = client.post('/posts/1/edit')
    assert response_wrong_user.status_code == 403

# def test_delete_post(client:testing.FlaskClient) -> None:
#     pass

def test_tags(client:testing.FlaskClient) -> None:
    # Page loads with all info
    response = client.get('/posts/tags/')
    assert response.status_code == 200
    assert all(x in response.text for x in ['depricated'])

def test_tag(client:testing.FlaskClient) -> None:
    # Page loads with all info
    response = client.get('/posts/tags/depricated')
    assert response.status_code == 200
    assert all(x in response.text
               for x in ['Underwater Basket Weaving 101',
                         'I put on my robe and wizard hat 🧙‍♂️',
                         '2 Comments', # update if more added to test db
                         'depricated'])

def test_comments(client:testing.FlaskClient) -> None:
    # Page loads with all info
    response = client.get('/posts/comments/')
    assert response.status_code == 200
    assert all(x in response.text
                         for x in [user0['username'], 'first', 'second'])

def test_add_comment(client:testing.FlaskClient) -> None:
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
    response_no_token = client.post('/posts/1/comments/add/',
                                    data={'content':'minato'})
    assert response_no_token.status_code == 400

    # Can't comment while logged out; redirects to login
    client.get('/logout') # do NOT move
    content_no_login = {'csrf_token': flask.g.csrf_token, 'content': 'fif'}
    response_no_login = client.post('/posts/1/comments/add/',
                                    data=content_no_login)
    assert response_no_login.status_code == 302
    assert response_no_login.location[:6] == '/login' # some params are appended

    # confirm comment was not pushed despite redirect
    all_comments = client.get('/posts/comments/')
    assert content_no_login['content'] not in all_comments.text

def test_delete_comment(client:testing.FlaskClient) -> None:
    # Setup - login
    client.get('/login') # creates CSRF token - do NOT move
    login_data = {'csrf_token': flask.g.csrf_token,
                                'user_email': user0['email'],
                                'password': user0['password']}
    client.post('/login', data=login_data)

    # Comment is deleted successfully
    response_valid = client.post('/posts/comments/1/delete/',
                                 follow_redirects=True)
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
    assert 'second' in all_comments.text # confirm not deleted despite redirect

    # Can't delete comment while logged in as another user
    login_data = {'csrf_token': flask.g.csrf_token,
                                'user_email': user1['email'],
                                'password': user1['password']}
    client.post('/login', data=login_data)
    response_wrong_user = client.post('/posts/comments/2/delete/')
    assert response_wrong_user.status_code == 403
