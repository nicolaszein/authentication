import peewee
import datetime
import secrets
from playhouse.signals import post_save
from authentication.exceptions import ActivationExpiredError
from authentication.models._shared import BaseModel
from authentication.handlers.send_activation_email import SendActivationEmail

ACTIVATION_EXPIRE_TIME = 7200


class User(BaseModel):
    full_name = peewee.CharField()
    email = peewee.CharField(unique=True)
    password = peewee.CharField()
    reset_password_token = peewee.CharField(null=True, unique=True)
    reset_password_token_created_at = peewee.DateTimeField(null=True)
    is_active = peewee.BooleanField(default=False)
    activation_token = peewee.CharField(null=True, unique=True)
    activation_token_created_at = peewee.DateTimeField(null=True)

    @property
    def activation_expire_date(self):
        return self.activation_token_created_at + datetime.timedelta(seconds=ACTIVATION_EXPIRE_TIME)

    def generate_activation(self):
        self.activation_token = secrets.token_urlsafe(16)
        self.activation_token_created_at = datetime.datetime.now()

    def activate(self):
        if datetime.datetime.now() > self.activation_expire_date:
            raise ActivationExpiredError(f'Activation for user {self.id} expired')

        self.is_active = True
        self.activation_token = None
        self.activation_token_created_at = None

    def generate_reset_password_token(self):
        self.reset_password_token = secrets.token_urlsafe(16)
        self.reset_password_token_created_at = datetime.datetime.now()

    def reset_password(self, password):
        self.reset_password_token = None
        self.reset_password_token_created_at = None
        self.password = password


@post_save(sender=User)
def send_activation_email(sender, instance, created):
    if not created:
        return None

    SendActivationEmail().execute(user=instance)
