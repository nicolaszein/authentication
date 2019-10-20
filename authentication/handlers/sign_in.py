from peewee import DoesNotExist
from authentication.settings import TOKEN_EXPIRATION_TIME
from authentication.exceptions import InvalidCredentialsError
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.services.authentication import Authentication as AuthenticationService
from authentication.services.token import Token as TokenService
from authentication.dtos.user import User as UserDto
from authentication.dtos.sign_in import SignIn as SignInDto
from authentication.models.user import User


class SignIn(BaseHandler):

    def __init__(self):
        self.__authentication_service = AuthenticationService
        self.__token_service = TokenService

    def execute(self, email, password):
        try:
            user = User.get(User.email == email)
        except DoesNotExist:
            raise InvalidCredentialsError(f'User with email {email} does not exist!')

        if not self.__valid_password(user, password):
            raise InvalidCredentialsError(f'Wrong password for {email}')

        user_dto = UserDto(id=str(user.id), full_name=user.full_name, email=user.email)

        token = self.__token_service.generate_token(user=user_dto)
        refresh_token = self.__token_service.generate_refresh_token(user=user_dto)

        return SignInDto(
            access_token=token,
            refresh_token=refresh_token,
            expires_in=TOKEN_EXPIRATION_TIME,
            token_type='Bearer'
        )

    def __valid_password(self, user, password):
        return self.__authentication_service.validate_password(password, user.password.encode())
