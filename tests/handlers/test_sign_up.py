from unittest.mock import patch
from authentication.handlers.sign_up import SignUp


@patch('authentication.handlers.sign_up.AuthenticationService')
@patch('authentication.handlers.sign_up.User.save')
@patch('authentication.handlers.sign_up.User.generate_activation')
def test_sign_up(generate_activation_mock, save_mock, auth_service_mock):
    params = {
        'full_name': 'Foo Bar',
        'email': 'foo.bar@email.com',
        'password': 'a-secret'
    }
    auth_service_mock.hash_password.return_value = 'hashed_password'

    user = SignUp().execute(params)

    assert user.full_name == 'Foo Bar'
    assert user.email == 'foo.bar@email.com'
    assert user.password == 'hashed_password'
    auth_service_mock.hash_password.assert_called_once_with(password='a-secret')
    save_mock.assert_called_once_with(force_insert=True)
    assert generate_activation_mock.call_count == 1
