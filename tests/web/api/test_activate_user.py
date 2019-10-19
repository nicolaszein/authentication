import datetime
from tests.factories.user import UserFactory


def test_activate_without_activation_token(client):
    payload = {
        'activation_token': None,
    }

    response = client.post(
        '/api/users/activate',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['activation_token']


def test_activate_with_unknown_activation_token(client):
    payload = {
        'activation_token': 'unknown_token',
    }

    response = client.post(
        '/api/users/activate',
        json=payload
    )

    assert response.status_code == 404


def test_activate_with_expired_activation_token(client):
    expired_date = datetime.datetime.now() - datetime.timedelta(seconds=8000)
    user = UserFactory.create(
        activation_token_created_at=expired_date
    )
    payload = {
        'activation_token': user.activation_token,
    }

    response = client.post(
        '/api/users/activate',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['activation_token'] == 'Token expired'


def test_activate_ok(client):
    user = UserFactory.create()
    payload = {
        'activation_token': user.activation_token,
    }

    response = client.post(
        '/api/users/activate',
        json=payload
    )

    assert response.status_code == 204
