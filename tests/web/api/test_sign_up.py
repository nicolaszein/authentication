def test_sign_up_without_full_name(client):
    payload = {
        'full_name': None,
        'email': 'foo.bar@email.com',
        'password': 'a-secret'
    }

    response = client.post(
        '/api/sign-up',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['full_name']


def test_sign_up_without_email(client):
    payload = {
        'full_name': 'Foo Bar',
        'email': None,
        'password': 'a-secret'
    }

    response = client.post(
        '/api/sign-up',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['email']


def test_sign_up_without_password(client):
    payload = {
        'full_name': 'Foo Bar',
        'email': 'foo.bar@email.com',
        'password': None
    }

    response = client.post(
        '/api/sign-up',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['password']


def test_sign_up_with_password_lenght_less_than_4(client):
    payload = {
        'full_name': 'Foo Bar',
        'email': 'foo.bar@email.com',
        'password': '123'
    }

    response = client.post(
        '/api/sign-up',
        json=payload
    )

    assert response.status_code == 400
    assert response.json['errors']['password']


def test_sign_up_ok(client):
    payload = {
        'full_name': 'Foo Bar',
        'email': 'foo.bar@email.com',
        'password': 'a-secret'
    }

    response = client.post(
        '/api/sign-up',
        json=payload
    )

    response_data = response.json['data']
    assert response.status_code == 201
    assert response_data['id']
    assert response_data['full_name'] == 'Foo Bar'
    assert response_data['email'] == 'foo.bar@email.com'
