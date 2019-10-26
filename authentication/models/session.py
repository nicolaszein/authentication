import peewee
from authentication.models._shared.base_model import BaseModel
from authentication.models.user import User


class Session(BaseModel):
    user = peewee.ForeignKeyField(User, backref='sessions')
    refresh_token = peewee.CharField(index=True, unique=True)
