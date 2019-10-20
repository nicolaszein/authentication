import pytest
from unittest.mock import patch
from jwt.exceptions import InvalidSignatureError
from authentication.exceptions import InvalidCredentialsError
from authentication.handlers.refresh_token import RefreshToken


@patch('authentication.handlers.refresh_token.UserDto')
@patch('authentication.handlers.refresh_token.TokenService')
def test_refresh_token_success(token_service_mock, user_dto_mock):
    user_dto_mock.return_value = 'user_dto'
    data = dict(id='123', full_name='Foo Bar', email='foo.bar@email.com')
    token_service_mock.validate_refresh_token.return_value = data

    sign_in = RefreshToken().execute(refresh_token='token')

    token_service_mock.generate_token.assert_called_once_with(user='user_dto')
    token_service_mock.generate_refresh_token.assert_called_once_with(user='user_dto')
    assert sign_in.token_type == 'Bearer'


@patch('authentication.handlers.refresh_token.TokenService')
def test_refresh_token_with_invalid_signature(token_service_mock):
    token_service_mock.validate_refresh_token.side_effect = InvalidSignatureError

    with pytest.raises(InvalidCredentialsError):
        RefreshToken().execute(refresh_token='invalid_token')
