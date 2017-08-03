import pytest

from snippets.models import Snippet


@pytest.mark.django_db
def test_snippet_save(new_user):
    """
    Ensure Snippet model saves `highlighted` field
    """
    snippet = Snippet(title='$', code='needle', owner=new_user)
    snippet.save()

    assert '<!DOCTYPE' in snippet.highlighted
    assert 'needle' in snippet.highlighted
    assert str(snippet) == '$'
