from unittest.mock import patch
from grades.handlers.authentication.sign_up import SignUp


@patch('grades.handlers.authentication.sign_up.AuthenticationService')
@patch('grades.handlers.authentication.sign_up.User.save')
def test_sign_up(save_mock, auth_service_mock):
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
    save_mock.call_count == 1
