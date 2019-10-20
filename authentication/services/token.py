import jwt
import datetime
from authentication.settings import (
    JWT_SECRET_TOKEN, TOKEN_EXPIRATION_TIME,
    REFRESH_TOKEN_EXPIRATION_TIME
)


class RefreshTokenExpiredError(Exception):
    pass


class Token:

    @classmethod
    def generate_token(cls, user, expire_in=TOKEN_EXPIRATION_TIME):
        claims_data = cls.__build_claims_data(expire_in)
        data = {**claims_data, **user.to_dict()}

        token = cls.__build_token(data)

        return token.decode()

    @classmethod
    def generate_refresh_token(cls, user):
        claims_data = cls.__build_claims_data()
        data = {**claims_data, **user.to_dict()}

        token = cls.__build_token(data)

        return token.decode()

    @staticmethod
    def validate_token(token):
        jwt.decode(token, JWT_SECRET_TOKEN, algorithms=['HS256'])

    @classmethod
    def validate_refresh_token(cls, refresh_token):
        now = datetime.datetime.timestamp(datetime.datetime.now())
        data = jwt.decode(refresh_token, JWT_SECRET_TOKEN, algorithms=['HS256'])

        if now > cls.__refresh_token_expired_at(data['iat']):
            raise RefreshTokenExpiredError(f'Refresh token expired')

        return data

    @classmethod
    def __build_claims_data(cls, expire_in=None):
        now = datetime.datetime.now()

        claims_data = {
            'iat': datetime.datetime.timestamp(now),
            'iss': 'authentication_svc'
        }

        if expire_in:
            exp = now + datetime.timedelta(seconds=expire_in)
            claims_data['exp'] = datetime.datetime.timestamp(exp)

        return claims_data

    @classmethod
    def __build_token(cls, data):
        return jwt.encode(
            data,
            JWT_SECRET_TOKEN,
            algorithm='HS256'
        )

    @classmethod
    def __refresh_token_expired_at(cls, iat):
        created_at = datetime.datetime.fromtimestamp(iat)
        expired_at = created_at + datetime.timedelta(seconds=REFRESH_TOKEN_EXPIRATION_TIME)

        return datetime.datetime.timestamp(expired_at)
