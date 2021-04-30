import pytest

from echis import mongo_init
from tests.model.factories import FilterFactory


@pytest.fixture()
def client() -> None:
    mongo_init(test=True)


@pytest.fixture()
def filter_module() -> FilterFactory:
    return FilterFactory()
