from authentication.models.user import User as UserModel
from authentication.dtos.user import User


def test_user_attributes():
    user = User(
        id='123',
        full_name='John',
        email='john@email.com',
    )

    assert user.id == '123'
    assert user.full_name == 'John'
    assert user.email == 'john@email.com'


def test_user_to_dict():
    user = User(
        id='123',
        full_name='John',
        email='john@email.com',
    )

    assert user.to_dict() == {
        'id': '123',
        'full_name': 'John',
        'email': 'john@email.com'
    }


def test_from_user_model():
    user_model = UserModel(
        id='123',
        full_name='John',
        email='john@email.com'
    )

    user = User.from_user_model(user=user_model)

    assert user.id == '123'
    assert user.full_name == 'John'
    assert user.email == 'john@email.com'
