import jwt
from tests.factories.user import UserFactory
from authentication.models.session import Session


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


def test_sign_in_ok(client):
    user = UserFactory.create()
    Session(
        user=user,
        refresh_token='token_123'
    ).save(force_insert=True)
    payload = {
        'refresh_token': 'token_123'
    }

    response = client.post(
        '/api/sign-in/refresh',
        json=payload
    )

    response_data = response.json['data']
    assert 'refresh_token' not in response_data
    assert response.status_code == 200
    assert response_data['access_token']
    assert response_data['expires_in']
    assert response_data['token_type']
