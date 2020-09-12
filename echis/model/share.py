import uuid
from dataclasses import asdict
from datetime import datetime
from typing import List, Optional

import mongoengine as me

from echis.modules.share_playlist import Spotify, Deezer, AbstractShare, Share


def get_interface(name: str) -> AbstractShare:
    name_clear = name.strip().lower()
    client = {
        "spotify": Spotify(),
        "deezer": Deezer()
    }
    return client.get(name_clear, Deezer)


class SharedSongs(me.Document):
    record_id = me.UUIDField(default=uuid.uuid4(), required=False)
    title = me.StringField(required=False)
    rank = me.IntField(required=True)
    song_id = me.StringField(required=True)
    title = me.StringField(required=True)
    artist = me.StringField(required=False)
    cover = me.StringField(required=False)
    album = me.StringField(required=True)
    playlist_id = me.StringField(required=False)
    added_to_playlist = me.StringField(required=True)
    added_by = me.StringField(required=False)
    created_at = me.DateTimeField(default=datetime.utcnow)
    api = me.StringField(required=False)
    is_shared = me.BooleanField(default=False)

    @staticmethod
    def fetch_playlist() -> Optional[List[Share]]:
        get_playlists: List[Playlists] = Playlists.objects
        songs: List[Share] = []
        for playlist in get_playlists:
            client = get_interface(playlist.api)
            client.fetch(playlist_id=playlist.playlist_id)
            latest: Share = client.get_latest
            latest.added_by = playlist.user
            if latest:
                is_exists = SharedSongs.objects(song_id=latest.song_id, api=latest.api).count()
                if not is_exists:
                    create = SharedSongs(**asdict(latest))
                    create.is_shared = True
                    create.save()
                    songs.append(latest)
        return songs


class Playlists(me.Document):
    record_id = me.UUIDField(default=uuid.uuid4(), unique=True)
    playlist_id = me.StringField(required=True)
    user = me.StringField(required=True)
    api = me.StringField(required=True)
    is_active = me.BooleanField(default=True)
    created_at = me.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def add_playlist(playlist_id: str, username: str, api: str) -> str:
        is_exist = Playlists.objects(playlist_id=playlist_id).count()
        if not is_exist:
            client = get_interface(api)
            playlist_resolve = client.playlist_is_exists(playlist_id)
            if playlist_resolve:
                new_playlist = Playlists(playlist_id=playlist_id, user=username, api=api)
                new_playlist.save()
                return "Success, playlist has been added"
            else:
                return "Error, playlist not found"
        else:
            return "Error, playlist already exists"

    @staticmethod
    def remove_playlist(playlist_id: str, username: str, api: str) -> str:
        playlist = Playlists.objects(playlist_id=playlist_id, user=username, api=api).first()
        if playlist:
            playlist.delete()
            return "Success, playlist has been removed"
        return "Error, playlist not found"
