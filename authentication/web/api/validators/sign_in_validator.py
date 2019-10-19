from marshmallow import fields
from authentication.web.api.validators._shared.base_validator import BaseValidator


class SignInValidator(BaseValidator):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
