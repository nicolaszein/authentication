def test_sign_up_ok(client):
    payload = {
        'full_name': 'Foo Bar',
        'email': 'foo.bar@email.com',
        'password': 'a-secret'
    }

    response = client.post(
        '/api/v1/authentication/sign-up',
        json=payload
    )

    response_data = response.json
    assert response.status_code == 201
    assert response_data['full_name'] == 'Foo Bar'
    assert response_data['email'] == 'foo.bar@email.com'


def test_sign_up_bad_request(client):
    payload = {
        'full_name': None,
        'email': 'foo.bar@email.com',
        'password': 'a-secret'
    }

    response = client.post(
        '/api/v1/authentication/sign-up',
        json=payload
    )

    assert response.status_code == 400
