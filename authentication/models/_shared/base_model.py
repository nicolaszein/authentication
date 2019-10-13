import peewee
import datetime
import uuid
import inflection
from playhouse.signals import Model
from authentication.db import DATABASE as db


def define_table_name(model_class):
    model_name = model_class.__name__
    return inflection.tableize(model_name)


class BaseModel(Model):
    id = peewee.UUIDField(primary_key=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now())
    updated_at = peewee.DateTimeField()
    deleted_at = peewee.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()

        if not self.id:
            self.id = uuid.uuid4()

        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = db
        table_function = define_table_name
