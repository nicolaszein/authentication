from flask import Blueprint, request, jsonify
from authentication.web.api.validators.sign_up_validator import SignUpValidator
from authentication.handlers.sign_up import SignUp
from authentication.web.api.serializers.user_serializer import UserSerializer

app = Blueprint('authentication', __name__)

ENDPOINT_PREFIX = '/api'


@app.route(f'{ENDPOINT_PREFIX}/sign-up', methods=['POST'])
def sign_up():
    data = request.json

    valid_data = SignUpValidator().validate(data=data)
    user = SignUp().execute(valid_data)

    return jsonify(UserSerializer().serialize(user)), 201
