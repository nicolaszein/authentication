
from grades.web.api._shared.base_serializer import BaseSerializer


class CustomSerializer(BaseSerializer):
    class Meta:
        wrapper = 'tests'


def test_serializer_serialize_with_meta_wrapper():
    serializer = CustomSerializer()

    response = serializer.serialize(data={})

    assert response['tests'] == {}


def test_serializer_serialize_with_serialize_wrapper():
    serializer = CustomSerializer()

    response = serializer.serialize(data={}, wrapper='serialize_tests')

    assert response['serialize_tests'] == {}
