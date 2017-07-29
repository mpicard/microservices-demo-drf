import re
import pytest

from datetime import datetime
from dateutil import parser
from django.utils.six import BytesIO
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.parsers import JSONParser
from rest_framework.serializers import ValidationError

from snippets.serializers import SnippetSerializer
from snippets.models import Snippet


@pytest.fixture(scope="function")
def context_request(new_user):
    factory = APIRequestFactory()
    request = factory.get('/snippets/')
    force_authenticate(request, user=new_user)
    return request


def test_serialization(context_request, new_user, new_snippet):
    serializer = SnippetSerializer(
        new_snippet,
        context={'request': context_request})

    data  = serializer.data

    assert re.search(r'snippets\/\d+\/', data['url'])
    assert re.search(r'snippets\/\d+\/highlight\/', data['highlight'])
    assert data['owner'] == new_user.id
    assert data['code'] == 'import python'
    assert data['title'] == 'New Snippet'
    assert data['language'] == 'python3'
    assert data['style'] == 'monokai'
    for date in (data['created'], data['updated']):
        assert isinstance(parser.parse(date), datetime)


def test_deserialization():
    json = b'{"code": "import python"}'
    stream = BytesIO(json)
    data = JSONParser().parse(stream)
    # ^^^ Often a pytext.fixture to stay DRY

    serializer = SnippetSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data['code'] == 'import python'


def test_validation():
    serializer = SnippetSerializer(data={
        'title': 'hack',
        'code': 'not me'
    })
    with pytest.raises(ValidationError):
        assert serializer.is_valid(raise_exception=True)
