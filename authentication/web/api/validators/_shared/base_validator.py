from marshmallow import Schema, ValidationError, EXCLUDE

from authentication.exceptions import ValidatorError


class BaseValidator(Schema):

    @property
    def class_name(self):
        return self.__class__.__name__

    def validate(self, data):
        try:
            return self.load(data, unknown=EXCLUDE)
        except ValidationError as e:
            raise ValidatorError(
                message=f'Error on {self.class_name}',
                errors=e.messages
            )
