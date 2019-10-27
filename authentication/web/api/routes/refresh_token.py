from flask import request, jsonify

from authentication.web.api import app, ENDPOINT_PREFIX
from authentication.web.api.validators.refresh_token_validator import RefreshTokenValidator
from authentication.web.api.serializers.sign_in_serializer import SignInSerializer
from authentication.handlers.refresh_token import RefreshToken


@app.route(f'{ENDPOINT_PREFIX}/sign-in/refresh', methods=['POST'])
def sign_in_refresh():
    data = request.json

    valid_data = RefreshTokenValidator().validate(data=data)

    sign_in = RefreshToken().execute(**valid_data)

    return jsonify(SignInSerializer().serialize(sign_in)), 200
