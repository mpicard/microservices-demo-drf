from rest_framework import serializers

from snippets.models import Snippet


def validate_something(value):
    """
    Business logic: resuable validations
    """
    if value == 'not me':
        raise serializers.ValidationError("You can't do that!")
    return value


class SnippetListSerializer(serializers.ListSerializer):
    class Meta:
        model = Snippet
        fields = ('url', 'title')


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    code = serializers.CharField(validators=[validate_something])
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight',
        read_only=True,
        format=None)

    class Meta:
        list_serializer_class = SnippetListSerializer
        model = Snippet
        fields = ('title', 'code', 'linenos', 'language', 'style', 'highlight')
        read_only_fields = ('created', 'updated')

    def validate_title(self, title):
        """
        Business logic: validate a field like `title`
        """
        if 'hack' in title.lower():
            raise serializers.ValidationError("You can't post hacks!")
        return title
