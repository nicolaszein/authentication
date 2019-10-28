from authentication.dtos.token_data import TokenData


def test_token_data_attributes():
    token_data = TokenData(
        id='123',
        full_name='John',
        email='john@email.com',
        session_id='456'
    )

    assert token_data.id == '123'
    assert token_data.full_name == 'John'
    assert token_data.email == 'john@email.com'
    assert token_data.session_id == '456'


def test_token_data_to_dict():
    token_data = TokenData(
        id='123',
        full_name='John',
        email='john@email.com',
        session_id='456'
    )

    assert token_data.to_dict() == {
        'id': '123',
        'full_name': 'John',
        'email': 'john@email.com',
        'session_id': '456'
    }


def test_token_data_to_dict_without_session_id():
    token_data = TokenData(
        id='123',
        full_name='John',
        email='john@email.com'
    )

    assert token_data.to_dict() == {
        'id': '123',
        'full_name': 'John',
        'email': 'john@email.com'
    }
