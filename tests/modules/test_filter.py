import csv
import os
import pytest

from echis.main import settings
from echis.main.settings import ROOT_DIR
from echis.modules.filter import is_bad_word


class TestFilter:
    @pytest.fixture(autouse=True)
    def setup(self):
        with open(settings.FILTER, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["fuck"])
        self.path = settings.FILTER
        yield
        os.remove(self.path)

    def test_is_bad_word_get_true(self):
        is_bad = is_bad_word("fuck")
        assert is_bad

    def test_is_not_bad_word(self):
        is_bad = is_bad_word("random")
        assert not is_bad
