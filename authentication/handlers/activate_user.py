from authentication.handlers._shared.base_handler import BaseHandler
from authentication.models.user import User


class ActivateUser(BaseHandler):

    def execute(self, activation_token):
        user = User.get(User.activation_token == activation_token)

        user.activate()

        user.save()
