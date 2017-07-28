from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User

from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.models import Snippet


class SnippetViewSet(ModelViewSet):
    """
    Manage short snippets of code of a given language and style with syntax
    highlighting using pygments.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    @detail_route(renderer_classes=[StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        # /snippet/{id}/highlight
        snippet = self.get_object()
        return Response(snippet.highlighted)

    @list_route()
    def recent(self, request):
        # /snippet/recent
        recent = Snippet.objects.all().order_by('-updated')

        page = self.paginate_queryset(recent)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(ReadOnlyModelViewSet):
    """
    Manage User and related snippets.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
