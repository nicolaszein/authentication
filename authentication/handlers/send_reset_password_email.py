from authentication.settings import APP_HOST
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.services.sendgrid import Sendgrid as SendgridService


class SendResetPasswordEmail(BaseHandler):

    def __init__(self):
        self.__sendgrid_service = SendgridService()

    def execute(self, user):
        self.__sendgrid_service.send_message(
            to=user.email,
            subject='Criar nova senha',
            html_content=self.__build_html_content(user)
        )

    def __build_html_content(self, user):
        return (
            f'<p>Olá, <strong>{user.full_name}</strong></p>'
            '<p>Para criar uma nova senha acesse'
            f' {APP_HOST}/auth/reset-password?token={user.reset_password_token}'
            ' e preencha o formulário!</p>'
            '<p>Abraços,</p>'
        )
