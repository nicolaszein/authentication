from peewee import DoesNotExist
from authentication.handlers._shared.base_handler import BaseHandler
from authentication.models.session import Session


class SignOut(BaseHandler):

    def execute(self, session_id):
        if not session_id:
            return None

        try:
            session = Session.get(Session.id == session_id)
        except DoesNotExist:
            return None

        session.delete_instance()
