from peewee import DoesNotExist
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.models.user import User


class CreateResetPasswordToken(BaseHandler):

    def execute(self, email):
        try:
            user = User.get(User.email == email)
        except DoesNotExist:
            return None

        user.generate_reset_password_token()
        user.save()
