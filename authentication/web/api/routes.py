from flask import Blueprint, request, jsonify

from authentication.web.api.validators.sign_up_validator import SignUpValidator
from authentication.web.api.validators.activate_user_validator import ActivateUserValidator
from authentication.web.api.validators.sign_in_validator import SignInValidator
from authentication.web.api.validators.refresh_token_validator import RefreshTokenValidator

from authentication.web.api.serializers.user_serializer import UserSerializer
from authentication.web.api.serializers.sign_in_serializer import SignInSerializer

from authentication.handlers.sign_up import SignUp
from authentication.handlers.activate_user import ActivateUser
from authentication.handlers.sign_in import SignIn
from authentication.handlers.refresh_token import RefreshToken

from authentication.services.token import RefreshTokenExpiredError

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


@app.route(f'{ENDPOINT_PREFIX}/sign-in', methods=['POST'])
def sign_in():
    data = request.json

    valid_data = SignInValidator().validate(data=data)
    sign_in = SignIn().execute(**valid_data)

    return jsonify(SignInSerializer().serialize(sign_in)), 200


@app.route(f'{ENDPOINT_PREFIX}/sign-in/refresh', methods=['POST'])
def sign_in_refresh():
    data = request.json

    valid_data = RefreshTokenValidator().validate(data=data)

    try:
        sign_in = RefreshToken().execute(**valid_data)

        return jsonify(SignInSerializer().serialize(sign_in)), 200
    except RefreshTokenExpiredError:
        return jsonify(errors='Expired refresh token'), 401
