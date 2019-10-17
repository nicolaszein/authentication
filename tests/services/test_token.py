import datetime
from unittest.mock import patch
from freezegun import freeze_time
from authentication.settings import JWT_SECRET_TOKEN, TOKEN_EXPIRATION_TIME
from authentication.services.token import Token
from authentication.dtos.user import User

user_attributes = {
    "id": "123",
    "full_name": "John",
    "email": "john@email.com"
}


@freeze_time('2019-01-01 00:00:00')
@patch('authentication.services.token.jwt')
def test_generate_token(jwt_mock):
    user = User(**user_attributes)
    exp = datetime.datetime.now() + datetime.timedelta(seconds=TOKEN_EXPIRATION_TIME)
    iat = datetime.datetime.now()
    iss = 'authentication_svc'
    claims_data = {
        'exp': datetime.datetime.timestamp(exp),
        'iat': datetime.datetime.timestamp(iat),
        'iss': iss
    }
    expected_payload = {**claims_data, **user.to_dict()}

    Token.generate_token(user)

    jwt_mock.encode.assert_called_once_with(
        expected_payload,
        JWT_SECRET_TOKEN,
        algorithm='HS256'
    )


@freeze_time('2019-01-01 00:00:00')
@patch('authentication.services.token.jwt')
def test_generate_refresh_token(jwt_mock):
    user = User(**user_attributes)
    iat = datetime.datetime.now()
    iss = 'authentication_svc'
    claims_data = {
        'iat': datetime.datetime.timestamp(iat),
        'iss': iss
    }
    expected_payload = {**claims_data, **user.to_dict()}

    Token.generate_refresh_token(user)

    jwt_mock.encode.assert_called_once_with(
        expected_payload,
        JWT_SECRET_TOKEN,
        algorithm='HS256'
    )
