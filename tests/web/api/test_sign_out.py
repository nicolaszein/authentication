from tests.factories.user import UserFactory
from authentication.models.session import Session
from authentication.dtos.token_data import TokenData
from authentication.services.token import Token


def test_sign_out_ok(client):
    user = UserFactory.create()
    session = Session(
        user=user,
        refresh_token='token_123'
    )
    session.save(force_insert=True)
    token_data = TokenData(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        session_id=session.id
    )
    token = Token.generate_token(token_data=token_data)
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = client.post(
        '/api/sign-out',
        headers=headers
    )

    assert response.status_code == 204


def test_sign_out_without_authorization_header(client):
    response = client.post('/api/sign-out')

    assert response.status_code == 401


def test_sign_out_with_authorization_header_invalid(client):
    response = client.post(
        '/api/sign-out',
        headers={'Authorization': 'fdfidajifjafjda'}
    )

    assert response.status_code == 401
