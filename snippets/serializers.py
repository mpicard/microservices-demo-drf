"""
Serializers: serialize and validate data for responses and requests
"""
from django.contrib.auth.models import User

from rest_framework import serializers

from snippets.models import Snippet


def validate_something(value):
    """
    Business logic: resuable validations
    """
    if 'not me' in value.lower():
        raise serializers.ValidationError("You can't do that, man!")
    return value


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    code = serializers.CharField(
        validators=[validate_something],
        style={'base_template': 'textarea.html'})
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight',
        read_only=True,
        format='html')

    class Meta:
        model = Snippet
        exclude = ('highlighted',)
        read_only_fields = ('created', 'updated')

    def validate_title(self, title):
        """
        Business logic: validate a field like `title`
        """
        if 'hack' in title.lower():
            raise serializers.ValidationError("You can't post hacks!")
        return title


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # Related via URL:
    snippets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='snippet-detail',
        read_only=True)
    # Nested with JSON:
    # snippets = SnippetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


"""
Build-in fields:

Boolean
NullBoolean
Char
Email
Regex
Slug
URL
UUID
FilePath
IPAddress
Integer
Float
Decimal
DateTime
Date
Time
Duration
Choice
MultipleChoice
File
Image
List
Dict
JSON
ReadOnly
Hidden
Model
SerializerMethod
*or custom fields...*
"""
