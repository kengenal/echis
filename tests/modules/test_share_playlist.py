import os
from typing import Dict

import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch

from echis.modules.share_playlist import Deezer, Share, Spotify, Youtube, AppleMusic
from echis.modules.token_authorization import SpotifyAuthorization


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
                        "link": "test",
                        "artist": {
                            "id": "407259",
                            "name": "New Medicine",
                        },
                        "album": {
                            "id": "8310422",
                            "title": "Breaking The model",
                            "cover_big": "https://e-cdns-images.dzcdn.net/images/cover"
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
                        "id": "test"
                    },
                    "track": {
                        "album": {
                            "artists": [
                                {
                                    "id": "dfasd2q1asda",
                                    "name": "test"
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
                            "name": "test"
                        },
                        "artists": [
                            {
                                "id": "asdasfwzs das",
                                "name": "test"
                            }
                        ],
                        "id": "asdagasddar213124",
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


class MockYoutubeData:
    @staticmethod
    def json() -> Dict:
        return {
            "items": [
                {
                    "id": "1234",
                    "snippet": {
                        "publishedAt": "2011-09-23T09:27:32Z",
                        "title": "HD Film Countdown Leader in 16x9 Ratio",
                        "description": "Beastly Exploitation Cinema's Film Leader Countdown.This 1080p HD Film ",
                        "thumbnails": {
                            "high": {
                                "url": "https://i.ytimg.com/vi/T0Jqdjbed40/maxresdefault.jpg",
                            }
                        },
                        "localized": {
                            "title": "HD Film Countdown Leader in 16x9 Ratio",
                            "description": "test"
                        }
                    }
                }
            ]
        }


class MockAppleMusicData:
    @staticmethod
    def json() -> Dict:
        return {
            "next": "/v1/catalog/pl/playlists/pl.u-4JomaDDua6rRpX8/tracks?offset=1",
            "data": [
                {
                    "id": "1363586737",
                    "type": "songs",
                    "href": "/v1/catalog/pl/songs/1363586737",
                    "attributes": {
                        "artwork": {
                            "width": 2000,
                            "height": 2000,
                            "url": "https://is4-ssl.mzstatic.com/image/thumb/Music124/v4/e8/de/1c/img.jpg/{w}x{h}bb.jpeg",
                            "bgColor": "0f0f0d",
                            "textColor1": "d7d3f4",
                            "textColor2": "cfced8",
                            "textColor3": "afacc6",
                            "textColor4": "a8a7af"
                        },
                        "artistName": "Jonathan Davis",
                        "url": "https://music.apple.com/pl/album/test/",
                        "discNumber": 1,
                        "genreNames": [
                            "Rock",
                            "Music"
                        ],
                        "durationInMillis": 172899,
                        "releaseDate": "2018-05-25",
                        "name": "Everyone",
                        "isrc": "m2kj13n",
                        "hasLyrics": True,
                        "albumName": "Album name",
                        "playParams": {
                            "id": "123123123",
                            "kind": "song"
                        },
                        "trackNumber": 3,
                        "composerName": "Random Artist"
                    }
                }
            ]
        }

    @property
    def status_code(self) -> int:
        return 200


class PlaylistNotFoundMock:
    @staticmethod
    def json() -> Dict:
        return {"error": {"status": 404}}

    @property
    def status_code(self) -> int:
        return 404


class PlaylistExistMock:
    @staticmethod
    def json() -> Dict:
        return {"random_playlist": {"status": 200}}

    @property
    def status_code(self) -> int:
        return 200


@pytest.fixture()
def deezer() -> Deezer:
    return Deezer()


@pytest.fixture()
def spotify() -> Spotify:
    return Spotify()


@pytest.fixture()
def youtube() -> Youtube:
    return Youtube()


def mock_apple_music_data(*args, **kwargs) -> MockAppleMusicData:
    return MockAppleMusicData()


def mock_get_empty_data(*args, **kwargs) -> MockResponseWithNoData:
    return MockResponseWithNoData()


def mock_with_data(*args, **kwargs) -> MockResponseWithData:
    return MockResponseWithData()


def mock_spotify_get_with_data(*args, **kwargs) -> MockSpotifyData:
    return MockSpotifyData()


def mock_youtube_get_with_data(*args, **kwargs) -> MockYoutubeData:
    return MockYoutubeData()


def mock_token(*args, **kwargs):
    return "123"


def mock_get_video(*args, **kwargs):
    return "134"


class TestDeezer:
    def test_deezer_with_get_last_from_deezer(self, monkeypatch: MonkeyPatch, deezer: Deezer):
        monkeypatch.setattr(requests, "get", mock_with_data)
        deezer.fetch(playlist_id=45489721)
        last = deezer.get_latest

        assert last.title is not None
        assert last.song_id is not None
        assert isinstance(last, Share)

    def test_get_latest_with_no_return_data_from_deezer(self, monkeypatch: MonkeyPatch, deezer: Deezer):
        monkeypatch.setattr(requests, "get", mock_get_empty_data)

        with pytest.raises(Exception) as exception_meme:
            deezer.fetch(playlist_id=45489721)
            _ = deezer.get_latest
            assert exception_meme.value == "Cannot download playlist"

    @pytest.mark.parametrize("take, expect", (
            [PlaylistNotFoundMock(), False],
            [PlaylistExistMock(), True]
    ))
    def test_deezer_check_playlist_for_deezer(self, monkeypatch: MonkeyPatch, deezer: Deezer, take, expect):
        def get_mock(*args, **kwargs):
            return take

        monkeypatch.setattr(requests, "get", get_mock)
        is_exist = deezer.playlist_is_exists("908622995")

        assert is_exist is expect


class TestSpotify:
    def test_get_lasted_with_data_from_spotify(self, monkeypatch: MonkeyPatch, spotify: Spotify):
        monkeypatch.setattr(SpotifyAuthorization, "get_token", mock_token)
        monkeypatch.setattr(requests, "get", mock_spotify_get_with_data)
        spotify.fetch(playlist_id="sdij9iuqsajhd")
        last = spotify.get_latest

        assert last.title is not None
        assert last.song_id is not None
        assert isinstance(last, Share)

    def test_get_latest_with_no_return_data_from_spotify(self, monkeypatch: MonkeyPatch, spotify: Spotify):
        monkeypatch.setattr(requests, "get", mock_get_empty_data)
        with pytest.raises(Exception) as exception_meme:
            spotify.fetch(playlist_id="sdij9iuqsajhd")
            _ = deezer.get_latest
            assert exception_meme.value == "Cannot download playlist"

    @pytest.mark.parametrize("take, expect", (
            [PlaylistNotFoundMock(), False],
            [PlaylistExistMock(), True]
    ))
    def test_check_playlist_for_spotify(self, monkeypatch: MonkeyPatch, spotify: Spotify, take, expect):
        def get_mock(*args, **kwargs):
            return take

        monkeypatch.setattr(requests, "get", get_mock)
        monkeypatch.setattr(SpotifyAuthorization, "get_token", mock_token)
        is_exist = spotify.playlist_is_exists("908622995")

        assert is_exist is expect


class TestYoutube:
    def test_get_lasted_with_data_from_youtube(self, monkeypatch: MonkeyPatch, youtube: Youtube):
        monkeypatch.setattr(requests, "get", mock_youtube_get_with_data)
        monkeypatch.setattr(Youtube, "get_token", mock_token)
        youtube.fetch(playlist_id="sdij9iuqsajhd", owner="testowner")
        last = youtube.get_latest

        assert last.title is not None
        assert last.song_id is not None
        assert isinstance(last, Share)

    def test_get_playlist_with_empty_video_id(self, monkeypatch: MonkeyPatch, youtube: Youtube):
        with pytest.raises(Exception) as error:
            monkeypatch.setattr(requests, "get", mock_youtube_get_with_data)
            monkeypatch.setattr(Youtube, "get_token", mock_token)

            youtube.fetch(playlist_id="sdij9iuqsajhd", owner="testowner")
            _ = youtube.get_latest
            assert error.value == "Youtube token is empty"

    def test_get_playlist_with_empty_token(self, monkeypatch: MonkeyPatch, youtube: Youtube):
        with pytest.raises(Exception) as error:
            monkeypatch.setattr(requests, "get", mock_youtube_get_with_data)
            monkeypatch.setattr(Youtube, "get_token", mock_token)

            youtube.fetch(playlist_id="sdij9iuqsajhd", owner="testowner")
            _ = youtube.get_latest
            assert error.value == "Youtube token is empty"


class TestAppleMusic:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.apple = AppleMusic()

    def test_get_lasted_with_data_from_apple_music(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(requests, "get", mock_apple_music_data)
        monkeypatch.setattr(self.apple, "get_token", mock_token)
        monkeypatch.setattr(Youtube, "get_video", mock_get_video)
        self.apple.fetch('random', owner="testowner")
        last = self.apple.get_latest

        assert last.title is not None
        assert last.song_id is not None
        assert isinstance(last, Share)

    def test_get_playlist_with_empty_token(self, monkeypatch: MonkeyPatch, youtube: Youtube):
        with pytest.raises(Exception) as error:
            os.environ["APPLE_SECRET_KEY"] = 123
            monkeypatch.setattr(requests, "get", mock_apple_music_data())
            monkeypatch.setattr(Youtube, "get_token", mock_token)

            youtube.fetch(playlist_id="sdij9iuqsajhd", owner="testowner")
            _ = youtube.get_latest
            assert error.value == "Youtube token is empty"

    @pytest.mark.parametrize("take, expect", (
            [PlaylistNotFoundMock(), False],
            [PlaylistExistMock(), True]
    ))
    def test_check_playlist_for_spotify(self, monkeypatch: MonkeyPatch, take, expect):
        def get_mock(*args, **kwargs):
            return take

        monkeypatch.setattr(self.apple, "get_songs", get_mock)
        monkeypatch.setattr(self.apple, "get_token", mock_token)
        is_exist = self.apple.playlist_is_exists("908622995")

        assert is_exist is expect
