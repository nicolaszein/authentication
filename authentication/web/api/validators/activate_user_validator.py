from marshmallow import fields, validate
from authentication.web.api.validators._shared.base_validator import BaseValidator


class ActivateUserValidator(BaseValidator):
    activation_token = fields.Str(required=True, validate=validate.Length(min=1))
