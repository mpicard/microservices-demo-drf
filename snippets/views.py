from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from snippets.serializers import SnippetSerializer, SnippetListSerializer
from snippets.models import Snippet


class SnippetViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    list_serializer_class = SnippetListSerializer

    @detail_route(renderer_classes=[StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    @list_route()
    def recent(self, request):
        recent = Snippet.objects.all().order_by('-updated')

        page = self.paginate_queryset(recent)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)
