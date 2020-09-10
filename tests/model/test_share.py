from typing import List
from unittest.mock import Mock

import pytest
from dotenv import load_dotenv

from echis.model.share import Playlists, SharedSongs
from echis.modules.mongo import mongo_init
from echis.modules.share_playlist import Deezer, Share


def get_last() -> List[Share]:
    return [Share(
        song_id='2141243213',
        title='Test',
        rank='411532',
        artist='yes',
        cover='https://e-cdns-images.dzcdn.net/images/cover/5bf40e45c5aba44a00c6afe697b0a5b9/250x250-000000-80-0-0.jpg ',
        album='Model',
        playlist_id='564216554',
        added_to_playlist='2019-09-05 13:57:11',
        added_by='random',
        api='deezer'
    )]


@pytest.fixture()
def con():
    load_dotenv()
    mongo_init(test=True)


@pytest.fixture()
def create_playlist():
    pl = Playlists(playlist_id="6492294924", user="test", api="deezer")
    pl.save()


def test_create_collection(con):
    pl = Playlists(playlist_id="6492294924", user="kengenal", api="deezer")
    pl.save()


def test_add_to_playlist(con):
    pl = Playlists(playlist_id="564216554", user="test", api="deezer")
    pl.save()

    mock = Deezer()
    mock.fetch = Mock(name="fetch")
    mock.playlists = get_last()
    songs = SharedSongs.fetch_playlist(client=mock)

    assert len(songs) > 0
    assert songs[0].playlist_id == "564216554"


def test_fetch_playlists_without_playlist_should_return_empty_array(con):
    mock = Deezer()
    mock.fetch = Mock(name="fetch")
    mock.playlists = get_last()
    songs = SharedSongs.fetch_playlist(client=mock)

    assert len(songs) == 0
