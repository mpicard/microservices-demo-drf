import pytest

from rest_framework.test import APIClient

from snippets.models import Snippet


@pytest.mark.django_db
@pytest.fixture(scope="function")
def new_user(django_user_model):
    user = django_user_model(username="test")
    user.save()
    return user


@pytest.fixture(scope="function")
def client(new_user):
    # Test session "singleton"
    client = APIClient()
    client.force_authenticate(user=new_user)
    return client


@pytest.mark.django_db
@pytest.fixture(scope="function")
def new_snippet(new_user):
    # Makes new snippet for each test module(test_*.py)
    new_snippet = Snippet(
        title="New Snippet",
        code="import python",
        linenos=False,
        language="python3",
        style="monokai",
        owner=new_user
    )
    new_snippet.save()
    return new_snippet
