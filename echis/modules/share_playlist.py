import os
import requests

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from echis.modules.token_authorization import SpotifyAuthorization


@dataclass
class Share:
    song_id: str
    title: str
    rank: str
    artist: str
    cover: str
    album: str
    playlist_id: str
    added_to_playlist: str
    added_by: str
    api: str


class AbstractShare(ABC):
    playlists: List[Share]

    @abstractmethod
    def fetch(self, playlist_id, limit: int = 1):
        pass

    @property
    def get_latest(self) -> Optional[Share]:
        if self.playlists:
            return self.playlists[0]
        return None

    @abstractmethod
    def playlist_is_exists(self, playlist_id: str):
        pass


class TokenRequired(ABC):
    @abstractmethod
    def get_token(self) -> str:
        pass


class Deezer(AbstractShare):
    url: str = "https://api.deezer.com/playlist/{}"

    def fetch(self, playlist_id: int, limit: int = 1):
        playlists: Optional[Dict] = {}
        try:
            rq = requests.get(self.url.format(playlist_id)).json()
            if "tracks" in rq:
                playlists = rq["tracks"]["data"]
        except KeyError:
            raise Exception("Cannot download playlist")
        except Exception as err:
            raise Exception("Cannot download playlist")
        songs: List[Share] = []
        if playlists:
            for playlist in playlists:
                timestamp = datetime.fromtimestamp(playlist["time_add"])
                songs.append(Share(
                    song_id=str(playlist["id"]),
                    title=playlist["title"],
                    rank=playlist["rank"],
                    artist=playlist["artist"]["name"],
                    cover=playlist["album"]["cover_big"],
                    album=playlist["album"]["title"],
                    playlist_id=str(rq["id"]),
                    added_to_playlist=timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    added_by=rq["creator"]["name"],
                    api="deezer"
                ))
        sorted_songs = sorted(songs, key=lambda x: x.added_to_playlist, reverse=True)
        self.playlists = sorted_songs

    def playlist_is_exists(self, playlist_id: str) -> bool:
        try:
            rq = requests.get(self.url.format(playlist_id))
            if "error" in rq.json():
                return False
            return True
        except ConnectionError as error:
            raise ConnectionError(error)


class Spotify(AbstractShare, TokenRequired):
    def __init__(self):
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.token = SpotifyAuthorization(client_id=client_id, client_secret=client_secret)
        self.url = "https://api.spotify.com/v1/playlists/{}/tracks?&limit={}&market={" \
                   "}&fields=artist%3Btitle%3Bimages%3Bid%3Bpopularity%3Bname%3Badded_at& "

    def fetch(self, playlist_id: str, limit: int = 1):
        playlists: Optional[Dict] = []
        market = os.getenv('SPOTIFY_MARKET')
        try:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            rq = requests.get(self.url.format(playlist_id, limit, market), headers=headers).json()
            if "items" in rq:
                playlists = rq["items"]
        except KeyError:
            raise Exception("Cannot download playlist")
        except Exception as error:
            print(error)
            raise Exception("Cannot download playlist")
        songs: List[Share] = []
        if rq and playlists:
            for playlist in playlists:
                songs.append(Share(
                    song_id=str(playlist["track"]["id"]),
                    artist=playlist['track']["album"]["artists"][0]["name"],
                    title=playlist["track"]["name"],
                    cover=[x for x in playlist["track"]["album"]["images"] if x['height'] == 640][0]["url"],
                    rank=playlist["track"]["popularity"],
                    album=playlist["track"]["album"]["name"],
                    playlist_id=str(playlist["track"]["album"]["id"]),
                    added_to_playlist=playlist["added_at"],
                    added_by=playlist["added_by"]["id"],
                    api="spotify"
                ))
        self.playlists = songs

    def playlist_is_exists(self, playlist_id: str):
        try:
            token = self.get_token()
            market_code = os.getenv("SPOTIFY_MARKET", "PL")
            headers = {
                "Authorization": f"Bearer {token}"
            }
            rq = requests.get(self.url.format(playlist_id, 1, market_code), headers=headers)
            if "error" in rq.json():
                return False
            return True
        except ConnectionError as error:
            raise ConnectionError(error)

    def get_token(self) -> str:
        if self.token.is_active:
            return self.token.token
        self.token.get_token()
        return self.token.token
