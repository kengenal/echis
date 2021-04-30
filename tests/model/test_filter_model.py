import os

import pytest

from echis.main import settings
from echis.model.filter_model import FilterModel
from tests.model.factories import FilterFactory


class TestFilterModel:
    @pytest.fixture(autouse=True)
    def setup(self, client: None, filter_module: FilterFactory) -> None:
        self.filter_module = filter_module

    def test_create_csv_file(self):
        FilterModel.generate_csv()

        assert os.path.exists(settings.FILTER)
        os.remove(settings.FILTER)

    def test_create_csv_file_with_empty_query(self):
        FilterModel.objects.delete()
        FilterModel.generate_csv()

        assert not os.path.exists(settings.FILTER)
