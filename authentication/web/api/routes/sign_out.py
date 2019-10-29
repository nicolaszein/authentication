from flask import request, jsonify

from authentication.web.api import app, ENDPOINT_PREFIX
from authentication.handlers.sign_out import SignOut
from authentication.services.token import Token


@app.route(f'{ENDPOINT_PREFIX}/sign-out', methods=['POST'])
def sign_out():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify(errors='Not authorized'), 401

    try:
        _, token = token.split('Bearer ')
    except ValueError:
        return jsonify(errors='Not authorized'), 401

    token_data = Token.validate_token(token=token)

    SignOut().execute(session_id=token_data.get('session_id'))

    return '', 204
