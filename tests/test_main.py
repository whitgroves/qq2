"""Test for the main routes of qq2."""
from flask import testing

def test_index(client:testing.FlaskClient) -> None:
    response = client.get('/')
    assert 'The current time is' in response.text

def test_about(client:testing.FlaskClient) -> None:
    response = client.get('/about')
    test_link = 'https://github.com/whitgroves/qq2'
    assert f'<a href="{test_link}" target="_blank">' in response.text
