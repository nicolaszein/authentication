import pytest
from unittest.mock import MagicMock
from peewee import DoesNotExist
from unittest.mock import patch
from authentication.models.user import User
from authentication.models.session import Session
from authentication.handlers.sign_in import SignIn
from authentication.exceptions import InvalidCredentialsError, UserNotActivatedError


@patch('authentication.handlers.sign_in.Session.save')
@patch('authentication.handlers.sign_in.TokenData')
@patch('authentication.handlers.sign_in.User.get')
@patch('authentication.handlers.sign_in.AuthenticationService')
@patch('authentication.handlers.sign_in.TokenService')
def test_sign_in_success(
            token_service_mock, auth_service_mock,
            get_mock, token_data_mock, session_save_mock
        ):

    user = User(email='foo.bar@email.com', password='a-secret', is_active=True)
    get_mock.return_value = user
    session_save_mock.return_value = Session(id='123', user=user)
    auth_service_mock.validate_password.return_value = True
    token_data_class_mock = MagicMock()
    token_data_mock.return_value = token_data_class_mock

    sign_in = SignIn().execute(
        email='foo.bar@email.com',
        password='a-secret'
    )

    token_service_mock.generate_token.assert_called_once_with(token_data=token_data_class_mock)
    token_service_mock.generate_refresh_token.assert_called_once_with(token_data=token_data_class_mock)
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
    user = User(email='foo.bar@email.com', password='a-secret', is_active=True)
    get_mock.return_value = user
    auth_service_mock.validate_password.return_value = False

    with pytest.raises(InvalidCredentialsError):
        SignIn().execute(
            email='foo.bar@email.com',
            password='wrong_password'
        )


@patch('authentication.handlers.sign_in.User.get')
def test_sign_in_user_not_activated(get_mock):
    user = User(email='foo.bar@email.com', password='a-secret', is_active=False)
    get_mock.return_value = user

    with pytest.raises(UserNotActivatedError):
        SignIn().execute(
            email='foo.bar@email.com',
            password='a-secret'
        )
