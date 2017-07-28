from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from snippets import views


# Regiseter Viewsets with Router
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
"""
| Method |      URL       |      Name      |     Action     |
|========|================|================|================|
| GET    | /snippets/     | snippet-list   | list           |
| POST   | /snippets/     | snippet-create | create         |
| GET    | /snippets/{id} | snippet-detail | retrieve       |
| PUT    | /snippets/{id} | snippet-detail | update         |
| PATCH  | /snippets/{id} | snippet-detail | partial_update |
| DELETE | /snippets/{id} | snippet-detail | destroy        |
"""

router.register(r'users', views.UserViewSet)
"""
Using viewsets can be a really useful abstraction.
It helps ensure that URL conventions will be consistent
across your API, minimizes the amount of code you need to write.
"""
urlpatterns = [
    url(r'^', include(router.urls)),
    # ...
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]
