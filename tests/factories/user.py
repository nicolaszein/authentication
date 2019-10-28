import datetime
import uuid
from authentication.models.user import User
from authentication.services.authentication import Authentication as AuthenticationService


def _build_user(**kwargs):
    now = datetime.datetime.now()

    user = User()
    user.full_name = kwargs.get('full_name', 'Antonie Russo')
    user.email = kwargs.get('email', 'antonie.russo@email.com')
    user.password = kwargs.get('password', 'a-secret')
    user.reset_password_token = kwargs.get('reset_password_token', uuid.uuid4())
    user.reset_password_token_created_at = kwargs.get('reset_password_token_created_at', now)
    user.is_active = kwargs.get('is_active', True)
    user.activation_token = kwargs.get('activation_token', uuid.uuid4())
    user.activation_token_created_at = kwargs.get('activation_token_created_at', now)
    user.save(force_insert=True)

    return user


class UserFactory:
    @classmethod
    def create(self, **kwargs):
        return _build_user(**kwargs)

    @classmethod
    def create_with_hashed_password(self, **kwargs):
        password = kwargs.get('password', 'a-secret')
        hash_password = AuthenticationService.hash_password(password)
        kwargs['password'] = hash_password

        return _build_user(**kwargs)
