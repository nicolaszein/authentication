import datetime
from unittest.mock import patch
from authentication.models.user import User


def test_user_attributes():
    params = {
        'full_name': 'Foo Bar',
        'email': 'foo@bar.com.br',
        'is_active': True,
        'password': 'a-secret',
        'reset_password_token': '123',
        'reset_password_token_created_at': datetime.datetime.now(),
        'activation_token': '456',
        'activation_token_created_at': datetime.datetime.now()
    }

    user = User(**params)

    assert user.full_name == params['full_name']
    assert user.email == params['email']
    assert user.is_active == params['is_active']
    assert user.password == params['password']
    assert user.reset_password_token == params['reset_password_token']
    assert user.reset_password_token_created_at == params['reset_password_token_created_at']
    assert user.activation_token == params['activation_token']
    assert user.activation_token_created_at == params['activation_token_created_at']


@patch('authentication.models.user.secrets')
def test_generate_activation(secrets_mock):
    secrets_mock.token_urlsafe.return_value = 'token'
    user = User()

    user.generate_activation()

    assert user.activation_token == 'token'
    assert user.activation_token_created_at
