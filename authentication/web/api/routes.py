from flask import Blueprint, request, jsonify
from authentication.web.api.validators.sign_up_validator import SignUpValidator
from authentication.web.api.validators.activate_user_validator import ActivateUserValidator
from authentication.handlers.sign_up import SignUp
from authentication.handlers.activate_user import ActivateUser
from authentication.web.api.serializers.user_serializer import UserSerializer
from authentication.models.user import ActivationExpiredError

app = Blueprint('authentication', __name__)

ENDPOINT_PREFIX = '/api'


@app.route(f'{ENDPOINT_PREFIX}/sign-up', methods=['POST'])
def sign_up():
    data = request.json

    valid_data = SignUpValidator().validate(data=data)
    user = SignUp().execute(valid_data)

    return jsonify(UserSerializer().serialize(user)), 201


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
