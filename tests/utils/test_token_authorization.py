from typing import Dict

import pytest
import requests

from echis.utils.token_authorization import SpotifyAuthorization


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
