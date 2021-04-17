import uuid
from dataclasses import asdict
from datetime import datetime
from typing import List, Optional

import mongoengine as me

from echis.main import settings
from echis.modules.share_playlist import Spotify, Deezer, Share, Youtube, AbstractShare, AppleMusic


def get_interface(name: str) -> Optional[AbstractShare]:
    name_clear = name.strip().lower()
    client = {
        "spotify": Spotify,
        "deezer": Deezer,
        "youtube": Youtube,
        "apple_music": AppleMusic,
    }
    get_client = client.get(name_clear, None)
    if get_client:
        return get_client()
    return None


class SharedSongs(me.Document):
    record_id = me.UUIDField(default=uuid.uuid4(), required=False)
    title = me.StringField(required=False)
    rank = me.IntField(required=False)
    song_id = me.StringField(required=True)
    artist = me.StringField(required=False)
    cover = me.StringField(required=False)
    album = me.StringField(required=True)
    playlist_id = me.StringField(required=False)
    added_to_playlist = me.StringField(required=True)
    added_by = me.StringField(required=False)
    created_at = me.DateTimeField(default=datetime.utcnow)
    api = me.StringField(required=False)
    link = me.StringField(required=False, default="")
    is_shared = me.BooleanField(default=False)

    @staticmethod
    def fetch_playlist() -> Optional[List[Share]]:
        get_playlists: List[Playlists] = Playlists.objects(is_active=True)
        songs: List[Share] = []
        for playlist in get_playlists:
            interface = get_interface(playlist.api)
            if interface:
                client = interface
                client.fetch(playlist_id=playlist.playlist_id)
                latest: Share = client.get_latest
                if latest:
                    latest.added_by = playlist.user
                    is_exists = SharedSongs.objects(song_id=latest.song_id, api=latest.api).count()
                    if not is_exists:
                        create = SharedSongs(**asdict(latest))
                        create.is_shared = True
                        create.save()
                        songs.append(latest)
                else:
                    raise Exception("Playlist not exist")
        return songs

    @staticmethod
    def get_songs_to_play() -> List[str]:
        share: List[Share] = SharedSongs.objects().order_by(settings.SHARE_DATE_SORTED)[:settings.QUEUE_LIMIT]
        songs = []
        for song in share:
            songs.append(f"{song.artist} {song.title}")
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
            if client:
                playlist_resolve = client.playlist_is_exists(playlist_id)
                if playlist_resolve:
                    new_playlist = Playlists(playlist_id=playlist_id, user=username, api=api)
                    new_playlist.save()
                    return "Success, playlist has been added"
                else:
                    return "Error, playlist not found"
        else:
            return "Error, playlist already exists, playlist must be public"

    @staticmethod
    def remove_playlist(playlist_id: str, username: str, api: str) -> str:
        playlist = Playlists.objects(playlist_id=playlist_id, user=username, api=api).first()
        if playlist:
            playlist.delete()
            return "Success, playlist has been removed"
        return "Error, playlist not found"
