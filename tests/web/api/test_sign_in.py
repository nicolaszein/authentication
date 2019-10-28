from tests.factories.user import UserFactory


def test_sign_in_without_email(client):
    payload = {
        'email': None,
        'password': 'a-secret'
    }

    response = client.post(
        '/api/sign-in',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['email']


def test_sign_in_without_password(client):
    payload = {
        'email': 'foo.bar@email.com',
        'password': None
    }

    response = client.post(
        '/api/sign-in',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['password']


def test_sign_in_with_unknown_user(client):
    payload = {
        'email': 'unknown@email.com',
        'password': 'a-secret'
    }

    response = client.post(
        '/api/sign-in',
        json=payload
    )

    assert response.status_code == 401
    assert response.json['errors'] == 'Invalid Credentials'


def test_sign_in_with_wrong_password(client):
    UserFactory.create_with_hashed_password(
        email='foo.bar@email.com',
        password='a-big-secret'
    )
    payload = {
        'email': 'foo.bar@email.com',
        'password': 'wrong'
    }

    response = client.post(
        '/api/sign-in',
        json=payload
    )

    assert response.status_code == 401
    assert response.json['errors'] == 'Invalid Credentials'


def test_sign_in_with_user_not_activated(client):
    UserFactory.create_with_hashed_password(
        email='foo.bar@email.com',
        password='a-big-secret',
        is_active=False
    )
    payload = {
        'email': 'foo.bar@email.com',
        'password': 'a-big-secret'
    }

    response = client.post(
        '/api/sign-in',
        json=payload
    )

    assert response.status_code == 401
    assert response.json['errors'] == 'Not activated'


def test_sign_in_ok(client):
    UserFactory.create_with_hashed_password(
        email='foo.bar@email.com',
        password='a-big-secret'
    )
    payload = {
        'email': 'foo.bar@email.com',
        'password': 'a-big-secret'
    }

    response = client.post(
        '/api/sign-in',
        json=payload
    )

    response_data = response.json['data']
    assert response.status_code == 200
    assert response_data['access_token']
    assert response_data['refresh_token']
    assert response_data['expires_in']
    assert response_data['token_type']
