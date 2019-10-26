import datetime
from authentication.models.user import User
from authentication.models.session import Session


def test_user_attributes():
    user = User(id='user_id')
    params = {
        'user': user,
        'refresh_token': 'token123',
        'created_at': datetime.datetime.now()
    }

    session = Session(**params)

    assert session.user.id == user.id
    assert session.refresh_token == params['refresh_token']
    assert session.created_at == params['created_at']
