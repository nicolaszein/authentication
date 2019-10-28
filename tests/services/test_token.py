import datetime
import pytest
import jwt
from unittest.mock import patch
from freezegun import freeze_time
from authentication.settings import JWT_SECRET_TOKEN, TOKEN_EXPIRATION_TIME
from authentication.services.token import Token
from authentication.dtos.token_data import TokenData

token_data_attributes = {
    "id": "123",
    "full_name": "John",
    "email": "john@email.com"
}


@freeze_time('2019-01-01 00:00:00')
@patch('authentication.services.token.jwt')
def test_generate_token(jwt_mock):
    token_data = TokenData(**token_data_attributes)
    exp = datetime.datetime.now() + datetime.timedelta(seconds=TOKEN_EXPIRATION_TIME)
    iat = datetime.datetime.now()
    iss = 'authentication_svc'
    claims_data = {
        'exp': datetime.datetime.timestamp(exp),
        'iat': datetime.datetime.timestamp(iat),
        'iss': iss
    }
    expected_payload = {**claims_data, **token_data.to_dict()}

    Token.generate_token(token_data)

    jwt_mock.encode.assert_called_once_with(
        expected_payload,
        JWT_SECRET_TOKEN,
        algorithm='HS256'
    )


@freeze_time('2019-01-01 00:00:00')
@patch('authentication.services.token.jwt')
def test_generate_token_without_expire_in(jwt_mock):
    token_data = TokenData(**token_data_attributes)
    iat = datetime.datetime.now()
    iss = 'authentication_svc'
    claims_data = {
        'iat': datetime.datetime.timestamp(iat),
        'iss': iss
    }
    expected_payload = {**claims_data, **token_data.to_dict()}

    Token.generate_token(token_data, expire_in=None)

    jwt_mock.encode.assert_called_once_with(
        expected_payload,
        JWT_SECRET_TOKEN,
        algorithm='HS256'
    )


@freeze_time('2019-01-01 00:00:00')
@patch('authentication.services.token.jwt')
def test_generate_refresh_token(jwt_mock):
    token_data = TokenData(**token_data_attributes)
    iat = datetime.datetime.now()
    iss = 'authentication_svc'
    claims_data = {
        'iat': datetime.datetime.timestamp(iat),
        'iss': iss
    }
    expected_payload = {**claims_data, **token_data.to_dict()}

    Token.generate_refresh_token(token_data)

    jwt_mock.encode.assert_called_once_with(
        expected_payload,
        JWT_SECRET_TOKEN,
        algorithm='HS256'
    )


@patch('authentication.services.token.jwt')
def test_validate_token(jwt_mock):
    token_data = TokenData(**token_data_attributes)
    token = Token.generate_token(token_data)

    Token.validate_token(token)

    jwt_mock.decode.assert_called_once_with(
        token,
        JWT_SECRET_TOKEN,
        algorithms=['HS256']
    )


def test_validate_expired_token():
    token_data = TokenData(**token_data_attributes)
    with freeze_time('2019-01-01 00:00:00'):
        token = Token.generate_token(token_data)

    with pytest.raises(jwt.ExpiredSignatureError):
        Token.validate_token(token)


def test_validate_token_with_invalid_signature():
    token = jwt.encode(
        dict(invalid='signature'),
        'invalid_signature',
        algorithm='HS256'
    )

    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        Token.validate_token(token)
