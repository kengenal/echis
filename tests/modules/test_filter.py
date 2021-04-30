import csv
import os
import pytest

from echis.main import settings
from echis.modules.filter import is_bad_word


class TestFilter:
    @pytest.fixture(autouse=True)
    def setup(self):
        with open(settings.FILTER, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["fuck"])
        self.path = settings.FILTER
        yield
        os.remove(self.path) if os.path.exists(self.path) else None

    def test_is_bad_word_get_true(self):
        is_bad = is_bad_word("fuck")
        assert is_bad

    def test_is_not_bad_word(self):
        is_bad = is_bad_word("random")
        assert not is_bad

    def test_file_not_exists_should_be_return_false(self):
        os.remove(self.path)
        is_bad = is_bad_word("fuck")
        assert not is_bad
