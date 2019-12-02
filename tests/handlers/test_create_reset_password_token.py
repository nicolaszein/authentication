from peewee import DoesNotExist
from unittest.mock import patch
from authentication.models.user import User
from authentication.handlers.create_reset_password_token import CreateResetPasswordToken


@patch('authentication.handlers.create_reset_password_token.User.save')
@patch('authentication.handlers.create_reset_password_token.User.get')
@patch('authentication.handlers.create_reset_password_token.SendResetPasswordEmail')
def test_create_reset_password_token_success(send_email_mock, get_mock, save_mock):
    user = User(reset_password_token=None, reset_password_token_created_at=None)
    get_mock.return_value = user

    CreateResetPasswordToken().execute(
        email=user.email
    )

    assert user.reset_password_token
    assert user.reset_password_token_created_at
    assert save_mock.call_count == 1
    send_email_mock().execute.assert_called_once_with(user=user)


@patch('authentication.handlers.create_reset_password_token.User.get')
def test_create_reset_password_token_with_unknown_email(get_mock):
    get_mock.side_effect = DoesNotExist()

    result = CreateResetPasswordToken().execute(
        email='unknown_email'
    )

    assert not result
