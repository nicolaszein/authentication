from unittest.mock import patch
from authentication.settings import APP_HOST
from authentication.models.user import User
from authentication.handlers.send_activation_email import SendActivationEmail


def build_html_content(user):
    return (
        f'<p>Olá, <strong>{user.full_name}</strong></p>'
        '<p>Para continuar acesse o link'
        f' {APP_HOST}/auth/activate?activation_token={user.activation_token}'
        ' e confirme seu e-mail!</p>'
        '<p>Abraços,</p>'
    )


@patch('authentication.handlers.send_activation_email.SendgridService')
def test_send_activation_email(sendgrid_service_mock):
    user = User()
    user.generate_activation()

    SendActivationEmail().execute(
        user=user
    )

    sendgrid_service_mock().send_message.assert_called_once_with(
        to=user.email,
        subject='Confirme seu e-mail',
        html_content=build_html_content(user)
    )
