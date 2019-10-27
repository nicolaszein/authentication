from flask import request, jsonify

from authentication.web.api import app, ENDPOINT_PREFIX
from authentication.web.api.validators.activate_user_validator import ActivateUserValidator
from authentication.handlers.activate_user import ActivateUser
from authentication.exceptions import ActivationExpiredError


@app.route(f'{ENDPOINT_PREFIX}/users/activate', methods=['POST'])
def activate_user():
    data = request.json

    valid_data = ActivateUserValidator().validate(data=data)
    try:
        ActivateUser().execute(
            activation_token=valid_data['activation_token']
        )

        return '', 204
    except ActivationExpiredError:
        return jsonify(errors={'activation_token': 'Token expired'}), 400
