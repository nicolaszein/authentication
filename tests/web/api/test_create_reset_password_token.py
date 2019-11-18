from tests.factories.user import UserFactory


def test_create_reset_password_token_without_email(client):
    payload = {
        'email': None,
    }

    response = client.post(
        '/api/reset-password',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['email']


def test_create_reset_password_token_non_email(client):
    payload = {
        'email': 'non_email',
    }

    response = client.post(
        '/api/reset-password',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['email']


def test_create_reset_password_token_with_unknown_email(client):
    payload = {
        'email': 'unknown@email.com',
    }

    response = client.post(
        '/api/reset-password',
        json=payload
    )

    assert response.status_code == 204


def test_create_reset_password_token_ok(client):
    user = UserFactory.create(reset_password_token=None)
    payload = {
        'email': user.email,
    }

    response = client.post(
        '/api/reset-password',
        json=payload
    )

    assert response.status_code == 204
