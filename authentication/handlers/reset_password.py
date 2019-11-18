from authentication.models.user import User
from authentication.services.authentication import Authentication as AuthenticationService
from authentication.handlers._shared.base_handler import BaseHandler


class ResetPassword(BaseHandler):

    def execute(self, reset_password_token, password):
        user = User.get(User.reset_password_token == reset_password_token)

        hashed_password = AuthenticationService.hash_password(password)
        user.reset_password(password=hashed_password)

        user.save()
