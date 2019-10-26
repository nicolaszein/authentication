import peewee
import datetime
import secrets
from authentication.exceptions import ActivationExpiredError
from authentication.models._shared import BaseModel

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
