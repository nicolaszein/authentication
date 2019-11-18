from marshmallow import fields, validate
from authentication.web.api.validators._shared.base_validator import BaseValidator


class ResetPasswordValidator(BaseValidator):
    password = fields.Str(required=True, validate=validate.Length(min=4))
