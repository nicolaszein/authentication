from unittest.mock import patch, MagicMock
from peewee import DoesNotExist
from authentication.handlers.sign_out import SignOut


@patch('authentication.handlers.refresh_token.Session.get')
def test_sign_out_success(session_get_mock):
    session_mock = MagicMock()
    session_get_mock.return_value = session_mock

    SignOut().execute(session_id='123')

    assert session_mock.delete_instance.call_count == 1


def test_sign_out_with_no_session_id():

    assert not SignOut().execute(session_id=None)


@patch('authentication.handlers.refresh_token.Session.get')
def test_sign_out_with_no_session(session_get_mock):
    session_get_mock.side_effect = DoesNotExist

    assert not SignOut().execute(session_id='123')
