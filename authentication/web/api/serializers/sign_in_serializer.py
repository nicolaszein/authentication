from authentication.web.api.serializers._shared.base_serializer import BaseSerializer


class SignInSerializer(BaseSerializer):

    class Meta():
        fields = ('access_token', 'refresh_token', 'expires_in', 'token_type')
