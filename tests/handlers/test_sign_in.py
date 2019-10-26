import pytest
from peewee import DoesNotExist
from unittest.mock import patch
from authentication.models.user import User
from authentication.handlers.sign_in import SignIn
from authentication.exceptions import InvalidCredentialsError


@patch('authentication.handlers.sign_in.Session.save')
@patch('authentication.handlers.sign_in.UserDto')
@patch('authentication.handlers.sign_in.User.get')
@patch('authentication.handlers.sign_in.AuthenticationService')
@patch('authentication.handlers.sign_in.TokenService')
def test_sign_in_success(
            token_service_mock, auth_service_mock,
            get_mock, user_dto_mock, session_save_mock
        ):
    user = User(email='foo.bar@email.com', password='a-secret')
    get_mock.return_value = user
    auth_service_mock.validate_password.return_value = True
    user_dto_mock.from_user_model.return_value = 'user_dto'

    sign_in = SignIn().execute(
        email='foo.bar@email.com',
        password='a-secret'
    )

    token_service_mock.generate_token.assert_called_once_with(user='user_dto')
    token_service_mock.generate_refresh_token.assert_called_once_with(user='user_dto')
    session_save_mock.assert_called_once_with(force_insert=True)
    assert sign_in.token_type == 'Bearer'


@patch('authentication.handlers.sign_in.User.get')
def test_sign_in_with_unknown_token(get_mock):
    get_mock.side_effect = DoesNotExist()

    with pytest.raises(InvalidCredentialsError):
        SignIn().execute(
            email='unknown@email.com',
            password='a-secret'
        )


@patch('authentication.handlers.sign_in.User.get')
@patch('authentication.handlers.sign_in.AuthenticationService')
def test_sign_in_with_wrong_password(auth_service_mock, get_mock):
    user = User(email='foo.bar@email.com', password='a-secret')
    get_mock.return_value = user
    auth_service_mock.validate_password.return_value = False

    with pytest.raises(InvalidCredentialsError):
        SignIn().execute(
            email='foo.bar@email.com',
            password='wrong_password'
        )
