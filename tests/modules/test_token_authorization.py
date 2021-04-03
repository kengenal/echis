from typing import Dict

import pytest
import requests

from echis.modules.exceptions import BadAppleMusicCredentialsException
from echis.modules.token_authorization import SpotifyAuthorization, AppleMusicToken


class MockTokenFromSpotify:
    @staticmethod
    def json() -> Dict:
        return {
            'access_token': 'tokedasdasdasd',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': ''
        }

    @property
    def status_code(self) -> int:
        return 200


class MockTokenFromSpotifyStatus400:
    @staticmethod
    def json() -> Dict:
        return {}

    @property
    def status_code(self) -> int:
        return 400


class MockTokenFromSpotifyEmpty:
    @staticmethod
    def json() -> Dict:
        return {}

    @property
    def status_code(self) -> int:
        return 200


@pytest.fixture()
def spotify_auth() -> SpotifyAuthorization:
    return SpotifyAuthorization(client_id="test", client_secret="test")


def mock_with_data(*args, **kwargs) -> MockTokenFromSpotify:
    return MockTokenFromSpotify()


def test_create_base(spotify_auth):
    get = spotify_auth.create_base64()

    assert isinstance(get, bytes)


def test_is_active_should_return_false(spotify_auth):
    assert spotify_auth.is_active is False


def test_get_token_with_complete_json(monkeypatch, spotify_auth):
    monkeypatch.setattr(requests, "post", mock_with_data)
    spotify_auth.get_token()
    assert spotify_auth.is_active
    assert spotify_auth.token == 'tokedasdasdasd'


def test_get_token_with_status_400_should_empty_token(monkeypatch, spotify_auth):
    def get_mock(*args, **kwargs):
        return MockTokenFromSpotifyStatus400()

    monkeypatch.setattr(requests, "post", get_mock)
    spotify_auth.get_token()

    assert spotify_auth.is_active is False
    assert spotify_auth.token is None


def test_get_token_should_be_raised_exception(monkeypatch, spotify_auth):
    def get_mock(*args, **kwargs):
        return MockTokenFromSpotifyEmpty()

    monkeypatch.setattr(requests, "post", get_mock)
    with pytest.raises(Exception) as exception:
        spotify_auth.get_token()
        assert exception.value == "Cannot get token from spotify"


class TestAppleMusicAuth:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._secret_key = """
-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgU208KCg/doqiSzsVF5sknVtYSgt8/3oiYGbvryIRrzSgCgYIKoZIzj0DAQehRANCAAQfrvDWizEnWAzB2Hx2r/NyvIBO6KGBDL7wkZoKnz4Sm4+1P1dhD9fVEhbsdoq9RKEf8dvzTOZMaC/iLqZFKSN6
-----END PRIVATE KEY-----
        """

    def test_create_token_with_correct_data_should_be_generate_token_without_any_exceptions(self):
        app = AppleMusicToken(self._secret_key, "123", "123")
        app.generate_token()

        assert app.token != ""
        assert "Authorization" in app.headers.keys()

    def test_token_with_broken_secret_key_should_be_raise_exception(self):
        with pytest.raises(BadAppleMusicCredentialsException) as err:
            app = AppleMusicToken("test", "123", "123")
            app.generate_token()
            assert "Check your secret key" in err.value
