import datetime
import pytest
from unittest.mock import patch
from authentication.exceptions import ActivationExpiredError
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


def test_activate():
    user = User(is_active=False)
    user.generate_activation()

    user.activate()

    assert user.is_active
    assert not user.activation_token
    assert not user.activation_token_created_at


def test_activate_expired():
    expired_date = datetime.datetime.now() - datetime.timedelta(seconds=8000)
    user = User(is_active=False)
    user.activation_token_created_at = expired_date

    with pytest.raises(ActivationExpiredError):
        user.activate()


@patch('authentication.models.user.secrets')
def test_generate_reset_password_token(secrets_mock):
    secrets_mock.token_urlsafe.return_value = 'reset_token'
    user = User(reset_password_token=None, reset_password_token_created_at=None)

    user.generate_reset_password_token()

    assert user.reset_password_token == 'reset_token'
    assert user.reset_password_token_created_at


def test_reset_password():
    user = User()
    user.generate_reset_password_token()

    user.reset_password(password='a-new-secret')

    assert not user.reset_password_token
    assert not user.reset_password_token_created_at
    assert user.password == 'a-new-secret'
