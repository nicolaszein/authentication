from unittest.mock import patch
from authentication.models.user import User
from authentication.handlers.send_reset_password_email import SendResetPasswordEmail


def build_html_content(user):
    return (
        f'<p>Olá, <strong>{user.full_name}</strong></p>'
        '<p>Para criar uma nova senha acesse'
        f' https://auth.nicolaszein.dev/auth/reset-password?token={user.reset_password_token}'
        ' e preencha o formulário!</p>'
        '<p>Abraços,</p>'
    )


@patch('authentication.handlers.send_reset_password_email.SendgridService')
def test_send_reset_password_email(sendgrid_service_mock):
    user = User()
    user.generate_reset_password_token()

    SendResetPasswordEmail().execute(
        user=user
    )

    sendgrid_service_mock().send_message.assert_called_once_with(
        to=user.email,
        subject='Criar nova senha',
        html_content=build_html_content(user)
    )
