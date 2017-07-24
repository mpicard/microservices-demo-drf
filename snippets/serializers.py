from rest_framework import serializers

from snippets.models import Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', read_only=True, format=None)

    class Meta:
        model = Snippet
        exclude = ('highlighted',)
        read_only_fields = ('created', 'updated')
