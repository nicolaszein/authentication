from peewee import DoesNotExist
from authentication.settings import TOKEN_EXPIRATION_TIME
from authentication.exceptions import InvalidCredentialsError
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.services.token import Token as TokenService
from authentication.models.session import Session
from authentication.dtos.user import User as UserDto
from authentication.dtos.sign_in import SignIn as SignInDto


class RefreshToken(BaseHandler):

    def __init__(self):
        self.__token_service = TokenService

    def execute(self, refresh_token):
        try:
            session = Session.get(Session.refresh_token == refresh_token)
        except DoesNotExist:
            raise InvalidCredentialsError(f'Invalid refresh_token')

        user_dto = UserDto.from_user_model(user=session.user)
        token = self.__token_service.generate_token(user=user_dto)

        return SignInDto(
            access_token=token,
            refresh_token=None,
            expires_in=TOKEN_EXPIRATION_TIME,
            token_type='Bearer'
        )
