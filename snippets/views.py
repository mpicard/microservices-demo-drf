from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from snippets.serializers import SnippetSerializer
from snippets.models import Snippet


class SnippetViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    @detail_route(renderer_classes=[StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
