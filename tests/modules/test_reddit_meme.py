from unittest.mock import patch, MagicMock

import pytest

from echis.modules.meme import RedditMeme


@pytest.fixture(scope="module")
def reddit() -> RedditMeme:
    return RedditMeme()


VALUE = [{"data": {
    "title": "test",
    "url": "test.com/image",
    "score": 5550,
    "author_fullname": "test",
    "post_hint": "img",
}}]


@patch.object(RedditMeme, 'query', return_value=VALUE)
def test_random_meme(mock: MagicMock, reddit: RedditMeme):
    assert 'title' in reddit.random[0]
    assert reddit.random[0]['title'] == "test"


@patch.object(RedditMeme, 'query', return_value=VALUE)
def test_hot_meme(mock: MagicMock, reddit: RedditMeme):
    assert 'title' in reddit.hot[0]
    assert reddit.hot[0]['title'] == "test"


@patch.object(RedditMeme, 'query', return_value=VALUE)
def test_fresh_meme(mock: MagicMock, reddit: RedditMeme):
    assert 'title' in reddit.hot[0]
    assert reddit.hot[0]['title'] == "test"


@patch.object(RedditMeme, 'query', return_value=[{}])
def test_random_meme_empty_value(mock: MagicMock, reddit: RedditMeme):
    with pytest.raises(Exception) as exception_meme:
        _ = reddit.random
        _ = reddit.hot
        _ = reddit.fresh
        assert exception_meme.value == "Problem with downloading meme"
