from peewee import DoesNotExist
from authentication.settings import TOKEN_EXPIRATION_TIME
from authentication.exceptions import InvalidCredentialsError
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.services.token import Token as TokenService
from authentication.models.session import Session
from authentication.dtos.token_data import TokenData
from authentication.dtos.sign_in import SignIn as SignInDto


class RefreshToken(BaseHandler):

    def __init__(self):
        self.__token_service = TokenService

    def execute(self, refresh_token):
        try:
            session = Session.get(Session.refresh_token == refresh_token)
        except DoesNotExist:
            raise InvalidCredentialsError(f'Invalid refresh_token')

        token_data = TokenData(
            id=session.user.id,
            full_name=session.user.full_name,
            email=session.user.email,
            session_id=session.id
        )
        token = self.__token_service.generate_token(token_data=token_data)

        return SignInDto(
            access_token=token,
            refresh_token=None,
            expires_in=TOKEN_EXPIRATION_TIME,
            token_type='Bearer'
        )
