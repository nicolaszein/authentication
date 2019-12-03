from authentication.settings import APP_HOST
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.services.sendgrid import Sendgrid as SendgridService


class SendActivationEmail(BaseHandler):

    def __init__(self):
        self.__sendgrid_service = SendgridService()

    def execute(self, user):
        self.__sendgrid_service.send_message(
            to=user.email,
            subject='Confirme seu e-mail',
            html_content=self.__build_html_content(user)
        )

    def __build_html_content(self, user):
        return (
            f'<p>Olá, <strong>{user.full_name}</strong></p>'
            '<p>Para continuar acesse o link'
            f' {APP_HOST}/auth/activate?activation_token={user.activation_token}'
            ' e confirme seu e-mail!</p>'
            '<p>Abraços,</p>'
        )
