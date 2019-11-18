from flask import request

from authentication.web.api import app, ENDPOINT_PREFIX
from authentication.web.api.validators.create_reset_password_token_validator import (
    CreateResetPasswordTokenValidator
)
from authentication.handlers.create_reset_password_token import CreateResetPasswordToken


@app.route(f'{ENDPOINT_PREFIX}/reset-password', methods=['POST'])
def create_reset_password_token():
    data = request.json
    valid_data = CreateResetPasswordTokenValidator().validate(data)

    CreateResetPasswordToken().execute(valid_data['email'])

    return '', 204
