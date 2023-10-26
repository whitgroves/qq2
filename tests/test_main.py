from .conftest import FlaskClient

def test_index(client:FlaskClient) -> None:
    response = client.get('/')
    assert 'The current time is' in response.text

def test_about(client:FlaskClient) -> None:
    response = client.get('/about')
    test_link = 'https://www.digitalocean.com/community/tutorial-series/how-to-create-web-sites-with-flask'
    assert f'<a href="{test_link}">{test_link}</a>' in response.text
