from flask import request

from authentication.web.api import app, ENDPOINT_PREFIX
from authentication.web.api.validators.reset_password_validator import ResetPasswordValidator
from authentication.handlers.reset_password import ResetPassword


@app.route(f'{ENDPOINT_PREFIX}/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.json
    valid_data = ResetPasswordValidator().validate(data)

    ResetPassword().execute(
        reset_password_token=token,
        password=valid_data['password']
    )

    return '', 204
