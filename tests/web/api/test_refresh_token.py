import jwt
from freezegun import freeze_time
from authentication.services.token import Token
from authentication.dtos.user import User


def test_sign_in_without_refresh_token(client):
    payload = {
        'refresh_token': None
    }

    response = client.post(
        '/api/sign-in/refresh',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['refresh_token']


def test_sign_in_with_invalid_token(client):
    refresh_token = jwt.encode({'invalid': 'token'}, 'wrong_key', algorithm='HS256')
    payload = {
        'refresh_token': refresh_token.decode()
    }

    response = client.post(
        '/api/sign-in/refresh',
        json=payload
    )

    assert response.status_code == 401
    assert response.json['errors'] == 'Invalid Credentials'


def test_sign_in_with_expired_token(client):
    user = User(id='123', full_name='Foo Bar', email='foo.bar@email.com')
    with freeze_time('2019-01-01 00:00:00'):
        refresh_token = Token.generate_refresh_token(user)
    payload = {
        'refresh_token': refresh_token
    }

    response = client.post(
        '/api/sign-in/refresh',
        json=payload
    )

    assert response.status_code == 401
    assert response.json['errors'] == 'Expired refresh token'


def test_sign_in_ok(client):
    user = User(id='123', full_name='Foo Bar', email='foo.bar@email.com')
    refresh_token = Token.generate_refresh_token(user)
    payload = {
        'refresh_token': refresh_token
    }

    response = client.post(
        '/api/sign-in/refresh',
        json=payload
    )

    response_data = response.json['data']
    assert response.status_code == 200
    assert response_data['access_token']
    assert response_data['refresh_token']
    assert response_data['expires_in']
    assert response_data['token_type']
