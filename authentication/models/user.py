import peewee
from authentication.models._shared import BaseModel


class User(BaseModel):
    full_name = peewee.CharField()
    email = peewee.CharField(unique=True)
    password = peewee.CharField()
    reset_password_token = peewee.CharField(null=True, unique=True)
    reset_password_token_created_at = peewee.DateTimeField(null=True)
    is_active = peewee.BooleanField(default=False)
