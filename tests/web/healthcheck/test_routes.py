def test_health_check(client):
    response = client.get('/health-check')

    assert response.data == b'Ok'
