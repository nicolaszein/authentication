from flask import Blueprint, request, jsonify
from grades.models.authentication.user import User
from grades.services.authentication import Authentication

app = Blueprint('authentication', __name__)

ENDPOINT_PREFIX = '/api/v1/authentication'


@app.route(f'{ENDPOINT_PREFIX}/sign-up', methods=['POST'])
def sign_up():
    hashed_password = Authentication().hash_password(request.json.get('password'))

    user = User()
    user.full_name = request.json.get('full_name')
    user.email = request.json.get('email')
    user.password = hashed_password
    user.save()

    return jsonify({
        'full_name': user.full_name,
        'email': user.email
    }), 201
