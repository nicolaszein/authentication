from grades.services.authentication import Authentication


def test_authentication_generate_password():
    password = 'a-secret'

    hashed_password = Authentication.hash_password(password)

    assert hashed_password
    assert hashed_password != password


def test_authentication_validate_password():
    password = 'a-secret'
    hashed_password = Authentication.hash_password(password)

    is_valid = Authentication.validate_password(password, hashed_password)

    assert is_valid
