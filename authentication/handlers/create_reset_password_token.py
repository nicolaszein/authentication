from peewee import DoesNotExist
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.handlers.send_reset_password_email import SendResetPasswordEmail
from authentication.models.user import User


class CreateResetPasswordToken(BaseHandler):

    def __init__(self):
        self.__send_reset_password_email = SendResetPasswordEmail()

    def execute(self, email):
        try:
            user = User.get(User.email == email)
        except DoesNotExist:
            return None

        user.generate_reset_password_token()
        user.save()

        self.__send_reset_password_email.execute(user=user)
