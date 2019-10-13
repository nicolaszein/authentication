from authentication.web.api.serializers.user_serializer import UserSerializer
from authentication.models.user import User


def test_serialize():
    user = User()

    response = UserSerializer().serialize(data=user)

    response_user = response.get('data', {})
    assert 'data' in response
    assert 'id' in response_user
    assert 'full_name' in response_user
    assert 'email' in response_user
