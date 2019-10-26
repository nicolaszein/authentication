import pytest
from unittest.mock import patch
from peewee import DoesNotExist
from authentication.exceptions import InvalidCredentialsError
from authentication.handlers.refresh_token import RefreshToken
from authentication.models.user import User
from authentication.models.session import Session


@patch('authentication.handlers.refresh_token.Session.get')
@patch('authentication.handlers.refresh_token.UserDto')
@patch('authentication.handlers.refresh_token.TokenService')
def test_refresh_token_success(
            token_service_mock, user_dto_mock, session_get_mock
        ):
    user_dto_mock.from_user_model.return_value = 'user_dto'
    user = User(id='123', full_name='Foo Bar', email='foo.bar@email.com')
    session = Session(user=user, refresh_token='token')
    session_get_mock.return_value = session

    sign_in = RefreshToken().execute(refresh_token='token')

    token_service_mock.generate_token.assert_called_once_with(user='user_dto')
    assert sign_in.token_type == 'Bearer'
    assert not sign_in.refresh_token


@patch('authentication.handlers.refresh_token.Session.get')
def test_refresh_token_with_invalid_signature(session_get_mock):
    session_get_mock.side_effect = DoesNotExist

    with pytest.raises(InvalidCredentialsError):
        RefreshToken().execute(refresh_token='invalid_token')
