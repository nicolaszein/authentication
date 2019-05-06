
from grades.web.api._shared.base_serializer import BaseSerializer


class UserSerializer(BaseSerializer):

    class Meta():
        fields = ('id', 'full_name', 'email')
