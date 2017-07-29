import pytest

from functools import reduce
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse


# By default your tests will fail if they try to access the database.
# Only if you explicitly request database access will this be allowed.
@pytest.mark.django_db
def test_list(client, new_snippet_set, settings):
    resp = client.get('/snippets/')

    assert resp.status_code == 200
    assert resp.json()['count'] == new_snippet_set.count()
    assert isinstance(resp.json()['results'], list)
    assert len(resp.json()['results']) == settings.REST_FRAMEWORK['PAGE_SIZE']


@pytest.mark.django_db
def test_retrieve(client, new_snippet):
    id = new_snippet.id
    resp = client.get(f'/snippets/{id}/')

    assert resp.status_code == 200


@pytest.mark.django_db
class TestIntegrations:

    def test_create(self, client, new_user):
        new_snippet = {
            'title': 'New Snippet',
            'code': 'import python',
            'language': 'python3',
            'style': 'monokai',
            'linenos': False
        }
        resp = client.post('/snippets/', new_snippet)

        assert resp.status_code == 201

    def test_update(self, client, new_snippet):
        id = new_snippet.id
        updated_snippet = {
            'title': 'Simple GET request',
            'code': """
                import requests
                r = requests.get('api.github.com/users/')
                print(r.json())"""
        }
        resp = client.put(f'/snippets/{id}/', updated_snippet)

        assert resp.status_code == 200
        assert resp.json()['title'] == 'Simple GET request'

    def test_destroy(self, client, new_snippet):
        id =  new_snippet.id
        resp = client.delete(reverse('snippet-detail', args=[id]))

        assert resp.status_code == 204

    def test_partial_update(self, client, new_snippet):
        id = new_snippet.id
        partial_snippet = {
            'title': 'New title'
        }
        resp = client.patch(
            reverse('snippet-detail', args=[id]),
            partial_snippet,
            format='json'
        )

        assert resp.status_code == 200

    def test_highlight(self, client, new_snippet):
        resp = client.get(reverse('snippet-highlight', args=[new_snippet.id]), format='text/html')

        assert resp.status_code == 200
        assert resp.accepted_media_type == 'text/html'
        assert resp.accepted_renderer.__class__.__name__ == 'StaticHTMLRenderer'

    def test_recent(self, client, new_snippet_set):
        resp = client.get(reverse('snippet-recent'))

        assert resp.status_code == 200
        assert resp.json()['count'] == new_snippet_set.count()
        results = resp.json()['results']
        expected_results = sorted(results, key=lambda a: a['updated'], reverse=True)
        assert results == expected_results

    def test_recent_page_is_none(self, client, new_snippet_set):
        resp = client.get(reverse('snippet-recent'), limit=100, page=10)

        assert resp.status_code == 200