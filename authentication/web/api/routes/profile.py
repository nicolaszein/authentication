from flask import request, jsonify

from authentication.web.api import app, ENDPOINT_PREFIX
from authentication.services.token import Token
from authentication.models.user import User
from authentication.web.api.serializers.user_serializer import UserSerializer


@app.route(f'{ENDPOINT_PREFIX}/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify(errors='Not authorized'), 401

    try:
        _, token = token.split('Bearer ')
    except ValueError:
        return jsonify(errors='Not authorized'), 401

    token_data = Token.validate_token(token=token)

    user = User.get(id=token_data['id'])

    return jsonify(UserSerializer().serialize(user)), 200
