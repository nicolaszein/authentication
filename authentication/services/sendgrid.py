from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from authentication.settings import SENDGRID_API_KEY


class Sendgrid:

    def __init__(self):
        self.__client = SendGridAPIClient(SENDGRID_API_KEY)

    def send_message(self, to, subject, html_content, from_email='no-reply@nicolaszein.dev'):
        message = Mail(
            from_email=from_email,
            to_emails=to,
            subject=subject,
            html_content=html_content
        )

        response = self.__client.send(message)
        return response
