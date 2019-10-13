import pytest
import datetime
from peewee import DoesNotExist
from unittest.mock import patch
from authentication.models.user import User, ActivationExpiredError
from authentication.handlers.activate_user import ActivateUser


@patch('authentication.handlers.activate_user.User.save')
@patch('authentication.handlers.activate_user.User.get')
def test_activate_user_success(get_mock, save_mock):
    user = User()
    user.generate_activation()
    get_mock.return_value = user

    ActivateUser().execute(
        activation_token=user.activation_token
    )

    assert user.is_active
    assert not user.activation_token
    assert not user.activation_token_created_at
    assert save_mock.call_count == 1


@patch('authentication.handlers.activate_user.User.get')
def test_activate_user_with_unknown_token(get_mock):
    get_mock.side_effect = DoesNotExist()

    with pytest.raises(DoesNotExist):
        ActivateUser().execute(
            activation_token='unknown_token'
        )


@patch('authentication.handlers.activate_user.User.get')
def test_activate_user_with_expired_token(get_mock):
    expired_date = datetime.datetime.now() - datetime.timedelta(seconds=8000)
    user = User()
    user.activation_token_created_at = expired_date
    get_mock.return_value = user

    with pytest.raises(ActivationExpiredError):
        ActivateUser().execute(
            activation_token=user.activation_token
        )
