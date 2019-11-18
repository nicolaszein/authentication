from tests.factories.user import UserFactory


def test_reset_password_without_password(client):
    payload = {
        'password': None,
    }

    response = client.post(
        '/api/reset-password/123456',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['password']


def test_reset_password_with_password_min_length(client):
    payload = {
        'password': 'abc',
    }

    response = client.post(
        '/api/reset-password/123456',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['password']


def test_reset_password_with_unknown_token(client):
    payload = {
        'password': 'a-secret',
    }

    response = client.post(
        '/api/reset-password/unknown-token',
        json=payload
    )

    assert response.status_code == 404


def test_reset_password_ok(client):
    user = UserFactory.create()
    payload = {
        'password': 'a-secret',
    }

    response = client.post(
        f'/api/reset-password/{user.reset_password_token}',
        json=payload
    )

    assert response.status_code == 204
