import pytest
import faker

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
        owner=new_user
    )
    new_snippet.save()
    return new_snippet


@pytest.mark.django_db
@pytest.fixture(scope="function")
def new_snippet_set(new_user):
    fake = faker.Factory.create()

    new_snippet_set = []
    for i in range(10):
        new_snippet_set.append(Snippet(
            title=fake.bs(),
            code=fake.text(max_nb_chars=200),
            linenos=fake.pybool(),
            language="python",
            style="monokai",
            owner=new_user
        ))
    Snippet.objects.bulk_create(new_snippet_set)

    return Snippet.objects.all()