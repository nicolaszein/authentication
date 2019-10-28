from flask import request, jsonify

from authentication.web.api import app, ENDPOINT_PREFIX
from authentication.web.api.serializers.sign_in_serializer import SignInSerializer
from authentication.web.api.validators.sign_in_validator import SignInValidator
from authentication.handlers.sign_in import SignIn
from authentication.exceptions import UserNotActivatedError


@app.route(f'{ENDPOINT_PREFIX}/sign-in', methods=['POST'])
def sign_in():
    data = request.json

    valid_data = SignInValidator().validate(data=data)
    try:
        sign_in = SignIn().execute(**valid_data)

        return jsonify(SignInSerializer().serialize(sign_in)), 200
    except UserNotActivatedError:
        return jsonify(errors='Not activated'), 401
