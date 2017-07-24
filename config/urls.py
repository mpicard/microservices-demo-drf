from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from snippets import views


# Regiseter Viewsets with Router
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)

"""
Using viewsets can be a really useful abstraction.
It helps ensure that URL conventions will be consistent
across your API, minimizes the amount of code you need to write,
and allows you to concentrate on the interactions and
representations your API provides rather than the specifics
of the URL conf.
"""
urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^admin/', admin.site.urls),
]
