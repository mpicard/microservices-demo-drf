import pytest

from rest_framework.test import APIClient


# By default your tests will fail if they try to access the database.
# Only if you explicitly request database access will this be allowed.
@pytest.mark.django_db
def test_list(client):
    resp = client.get('/snippets/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_get(client, new_snippet):
    id = new_snippet.id
    resp = client.get(f'/snippets/{id}/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create(client, new_user):
    new_snippet = {
        'title': 'New Snippet',
        'code': 'import python',
        'language': 'python3',
        'style': 'monokai',
        'linenos': False
    }
    resp = client.post('/snippets/', new_snippet, format='json')
    assert resp.status_code == 201