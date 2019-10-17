import jwt
import datetime
from authentication.settings import JWT_SECRET_TOKEN, TOKEN_EXPIRATION_TIME


class Token:

    @staticmethod
    def generate_token(user):
        now = datetime.datetime.now()
        exp = now + datetime.timedelta(seconds=TOKEN_EXPIRATION_TIME)

        claims_data = {
            'exp': datetime.datetime.timestamp(exp),
            'iat': datetime.datetime.timestamp(now),
            'iss': 'authentication_svc'
        }
        data = {**claims_data, **user.to_dict()}

        token = jwt.encode(
            data,
            JWT_SECRET_TOKEN,
            algorithm='HS256'
        )

        return token

    @staticmethod
    def generate_refresh_token(user):
        now = datetime.datetime.now()

        claims_data = {
            'iat': datetime.datetime.timestamp(now),
            'iss': 'authentication_svc'
        }
        data = {**claims_data, **user.to_dict()}

        token = jwt.encode(
            data,
            JWT_SECRET_TOKEN,
            algorithm='HS256'
        )

        return token
