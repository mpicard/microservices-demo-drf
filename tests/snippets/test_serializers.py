from pytest import raises

from rest_framework.serializers import ValidationError

from snippets.serializers import SnippetSerializer


def test_serialization():
    data = {
        'title': 'test',
        'code': 'import python',
        'linenos': 'false',
        'language': 'python3'
    }
    serializer = SnippetSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['title'] == 'test'
    assert serializer.validated_data['code'] == 'import python'
    assert serializer.validated_data['linenos'] is False
    assert serializer.validated_data['language'] == 'python3'


def test_validation():
    serializer = SnippetSerializer(data={
        'title': 'hack',
        'code': 'not me'
    })
    with raises(ValidationError):
        assert serializer.is_valid(raise_exception=True)
