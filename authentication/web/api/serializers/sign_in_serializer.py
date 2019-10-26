from marshmallow import post_dump
from authentication.web.api.serializers._shared.base_serializer import BaseSerializer


class SignInSerializer(BaseSerializer):

    class Meta():
        fields = ('access_token', 'refresh_token', 'expires_in', 'token_type')

    @post_dump
    def remove_null_refresh_token(self, data, **kwargs):
        if not data['refresh_token']:
            del data['refresh_token']
        return data
