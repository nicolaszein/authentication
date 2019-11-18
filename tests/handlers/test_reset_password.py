import pytest
from peewee import DoesNotExist
from unittest.mock import patch
from authentication.models.user import User
from authentication.handlers.reset_password import ResetPassword


@patch('authentication.handlers.reset_password.User.save')
@patch('authentication.handlers.reset_password.User.get')
@patch('authentication.handlers.reset_password.AuthenticationService')
def test_reset_password_success(authentication_service_mock, get_mock, save_mock):
    user = User()
    get_mock.return_value = user
    authentication_service_mock.hash_password.return_value = 'password_hashed'

    ResetPassword().execute(
        reset_password_token='123',
        password='new_password'
    )

    assert not user.reset_password_token
    assert not user.reset_password_token_created_at
    assert user.password == 'password_hashed'
    assert save_mock.call_count == 1


@patch('authentication.handlers.reset_password.User.get')
def test_reset_password_with_unknown_email(get_mock):
    get_mock.side_effect = DoesNotExist()

    with pytest.raises(DoesNotExist):
        ResetPassword().execute(
            reset_password_token='unknown',
            password='new_password'
        )
