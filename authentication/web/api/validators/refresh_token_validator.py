from marshmallow import fields
from authentication.web.api.validators._shared.base_validator import BaseValidator


class RefreshTokenValidator(BaseValidator):
    refresh_token = fields.Str(required=True)
