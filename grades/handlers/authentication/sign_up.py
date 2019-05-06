from grades.handlers._shared.base_handler import BaseHandler
from grades.services.authentication import Authentication as AuthenticationService
from grades.models.authentication.user import User


class SignUp(BaseHandler):

    def __init__(self):
        self.__authentication_service = AuthenticationService

    def execute(self, params):
        hashed_password = self.__authentication_service.hash_password(
            password=params.get('password')
        )

        user = User()
        user.full_name = params.get('full_name')
        user.email = params.get('email')
        user.password = hashed_password
        user.save()

        return user
