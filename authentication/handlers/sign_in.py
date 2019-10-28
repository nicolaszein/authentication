from peewee import DoesNotExist
from authentication.settings import TOKEN_EXPIRATION_TIME
from authentication.exceptions import InvalidCredentialsError, UserNotActivatedError
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.services.authentication import Authentication as AuthenticationService
from authentication.services.token import Token as TokenService
from authentication.dtos.user import User as UserDto
from authentication.dtos.sign_in import SignIn as SignInDto
from authentication.models.user import User
from authentication.models.session import Session


class SignIn(BaseHandler):

    def __init__(self):
        self.__authentication_service = AuthenticationService
        self.__token_service = TokenService

    def execute(self, email, password):
        try:
            user = User.get(User.email == email)
        except DoesNotExist:
            raise InvalidCredentialsError(f'User with email {email} does not exist!')

        if not user.is_active:
            raise UserNotActivatedError(f'User with email {email} not activated')

        if not self.__valid_password(user, password):
            raise InvalidCredentialsError(f'Wrong password for {email}')

        user_dto = UserDto.from_user_model(user=user)

        refresh_token = self.__token_service.generate_refresh_token(user=user_dto)
        Session(user=user, refresh_token=refresh_token).save(force_insert=True)

        token = self.__token_service.generate_token(user=user_dto)

        return SignInDto(
            access_token=token,
            refresh_token=refresh_token,
            expires_in=TOKEN_EXPIRATION_TIME,
            token_type='Bearer'
        )

    def __valid_password(self, user, password):
        return self.__authentication_service.validate_password(password, user.password.encode())
