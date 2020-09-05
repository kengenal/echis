import unittest
from typing import Dict

import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch
from dotenv import load_dotenv

from echis.share.deezer import Deezer, Share, Spotify


class MockResponseWithData:
    @staticmethod
    def json() -> Dict:
        return {
            "id": "6492294924",
            "type": "playlist",
            "creator": {
                "name": "random",
            },
            "tracks": {
                "data": [
                    {
                        "id": "82740060",
                        "title": "Fire Up The Night",
                        "rank": "411532",
                        "time_add": 1567684631,
                        "artist": {
                            "id": "407259",
                            "name": "New Medicine",
                        },
                        "album": {
                            "id": "8310422",
                            "title": "Breaking The Model",
                            "cover_medium": "https://e-cdns-images.dzcdn.net/images/cover"
                                            "/5bf40e45c5aba44a00c6afe697b0a5b9/250x250-000000-80-0-0.jpg "
                        }
                    }
                ],
            }
        }


class MockResponseWithNoData:
    @staticmethod
    def json() -> Dict:
        return {}


class MockSpotifyData:
    @staticmethod
    def json() -> Dict:
        return {
            "items": [
                {
                    "added_at": "2017-09-01T13:46:42Z",
                    "added_by": {
                        "id": "kengenal"
                    },
                    "track": {
                        "album": {
                            "artists": [
                                {
                                    "id": "2gK2vUsncaH9nrI7gQIYH5",
                                    "name": "Echoes The Fall"
                                }
                            ],
                            "id": "6gLBQlOZ3j7SND5BLbLkT7",
                            "images": [
                                {
                                    "height": 640,
                                    "url": "https://i.scdn.co/image/ab67616d0000b27377fedcd872b7ebaa93f80f23",
                                    "width": 640
                                }
                            ],
                            "name": "Echoes The Fall"
                        },
                        "artists": [
                            {
                                "id": "2gK2vUsncaH9nrI7gQIYH5",
                                "name": "Echoes The Fall"
                            }
                        ],
                        "id": "3w0gPebgY2Yrkedw9cpbVe",
                        "name": "This Is Not Goodbye",
                        "popularity": 42
                    }
                }
            ]
        }


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


@pytest.fixture()
def deezer() -> Deezer:
    return Deezer()


@pytest.fixture()
def spotify() -> Spotify:
    return Spotify()


def mock_get_empty_data(*args, **kwargs) -> MockResponseWithNoData:
    return MockResponseWithNoData()


def mock_with_data(*args, **kwargs) -> MockResponseWithData:
    return MockResponseWithData()


def test_deezer_with_get_last_from_deezer(monkeypatch: MonkeyPatch, deezer: Deezer):
    def mock_get(*args, **kwargs):
        return MockResponseWithData()

    monkeypatch.setattr(requests, "get", mock_get)
    deezer.fetch(playlist_id=45489721)
    last = deezer.get_latest

    assert last.title is not None
    assert last.id is not None
    assert isinstance(last, Share)


def test_get_latest_with_no_return_data_from_deezer(monkeypatch: MonkeyPatch, deezer: Deezer):
    monkeypatch.setattr(requests, "get", mock_get_empty_data)
    with pytest.raises(Exception) as exception_meme:
        deezer.fetch(playlist_id=45489721)
        _ = deezer.get_latest
        assert exception_meme.value == "Cannot download playlist"


def test_get_lasted_with_data_from_spotify(monkeypatch, spotify):
    def mock_get(*args, **kwargs):
        return MockSpotifyData()

    monkeypatch.setattr(requests, "get", mock_get)
    spotify.fetch(playlist_id="sdij9iuqsajhd", token="token")
    last = spotify.get_latest

    assert last.title is not None
    assert last.id is not None
    assert isinstance(last, Share)


def test_get_latest_with_no_return_data_from_spotify(monkeypatch, spotify):
    monkeypatch.setattr(requests, "get", mock_get_empty_data)
    with pytest.raises(Exception) as exception_meme:
        spotify.fetch(playlist_id="sdij9iuqsajhd", token="random token")
        _ = deezer.get_latest
        assert exception_meme.value == "Cannot download playlist"

