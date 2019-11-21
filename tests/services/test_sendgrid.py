from unittest.mock import patch
from authentication.services.sendgrid import Sendgrid


@patch('authentication.services.sendgrid.Mail')
@patch('authentication.services.sendgrid.SendGridAPIClient')
def test_send_message(sendgrid_client_mock, mail_mock):
    sendgrid = Sendgrid()
    mail_mock.return_value = 'mail_instance'

    sendgrid.send_message(
        to='foo.bar@email.com',
        subject='A subject',
        html_content='<div>Hello</div>',
        from_email='bar.foo@email.com'
    )

    mail_mock.assert_called_once_with(
        from_email='bar.foo@email.com',
        to_emails='foo.bar@email.com',
        subject='A subject',
        html_content='<div>Hello</div>'
    )
    sendgrid_client_mock().send.assert_called_once_with('mail_instance')
