import pytest

from echis.main import settings
from echis.modules.token import create_token


class TestCreateToken:
    def test_create_token_without_algorithm_should_be_raise_exception(self):
        with pytest.raises(Exception) as err:
            settings.TOKEN_ALGORITHM = None
            _ = create_token({"test": "test"})

            assert err.value == "Secret cannot be null"

    def test_create_token_without_secret_should_be_raise_exception(self):
        with pytest.raises(Exception) as err:
            settings.TOKEN_SECRET = None
            _ = create_token({"test": "test"})

            assert err.value == "Data cannot be null"

    def test_create_token_correct_data(self):
        settings.TOKEN_SECRET = "213123"
        settings.TOKEN_ALGORITHM = "HS256"
        token = create_token({"test": "test"})

        assert isinstance(token, str)
