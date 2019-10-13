from authentication.web.api.serializers._shared.base_serializer import BaseSerializer


class UserSerializer(BaseSerializer):

    class Meta():
        fields = ('id', 'full_name', 'email')
