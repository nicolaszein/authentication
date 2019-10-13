from marshmallow import fields, validate
from authentication.web.api.validators._shared.base_validator import BaseValidator


class SignUpValidator(BaseValidator):
    full_name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=4))
