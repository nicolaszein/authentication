from marshmallow import fields
from authentication.web.api.validators._shared.base_validator import BaseValidator


class CreateResetPasswordTokenValidator(BaseValidator):
    email = fields.Email(required=True)
