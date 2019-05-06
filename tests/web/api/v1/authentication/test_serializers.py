from grades.web.api.v1.authentication.serializers import UserSerializer
from grades.models.authentication.user import User


def test_representer_render():
    user = User()

    response = UserSerializer().serialize(data=user)

    response_user = response.get('data', {})
    assert 'data' in response
    assert 'id' in response_user
    assert 'full_name' in response_user
    assert 'email' in response_user
