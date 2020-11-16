import os
import pytest

from echis.modules.filter import is_bad_word


@pytest.fixture()
def path():
    return os.path.abspath("echis/csv/bad_words.csv")


def test_is_bad_word_get_true(path: str):
    is_bad = is_bad_word("fuck", path=path)
    assert is_bad


def test_is_not_bad_word(path: str):
    is_bad = is_bad_word("random", path=path)
    assert not is_bad
