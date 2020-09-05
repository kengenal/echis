import os
import requests

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from echis.utils.token_authorization import SpotifyAuthorization


@dataclass
class Share:
    id: str
    title: str
    rank: str
    artist: str
    cover: str
    album: str
    playlist_id: str
    added_to_playlist: str
    added_by: str


class AbstractShare(ABC):
    playlist: List[Share]

    @abstractmethod
    def fetch(self, playlist_id):
        pass

    @property
    def get_latest(self) -> Optional[Share]:
        if self.playlist:
            return sorted(self.playlist, key=lambda x: x.added_to_playlist, reverse=True)[0]
        return None


class Deezer(AbstractShare):
    def fetch(self, playlist_id: int, token: Optional[str] = None):
        playlists: Optional[Dict]
        try:
            rq = requests.get(f"https://api.deezer.com/playlist/{playlist_id}").json()
            playlists = rq["tracks"]["data"]
        except KeyError:
            raise Exception("Cannot download playlist")
        except Exception:
            raise Exception("Cannot download playlist")
        songs: List[Share] = []
        if playlists:
            for playlist in playlists:
                timestamp = datetime.fromtimestamp(playlist["time_add"])
                songs.append(Share(
                    id=str(playlist["id"]),
                    title=playlist["title"],
                    rank=playlist["rank"],
                    artist=playlist["artist"]["name"],
                    cover=playlist["album"]["cover_medium"],
                    album=playlist["album"]["title"],
                    playlist_id=str(rq["id"]),
                    added_to_playlist=timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    added_by=rq["creator"]["name"]
                ))
        self.playlist = songs


class Spotify(AbstractShare):
    def __init__(self):
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_sercet = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.token = SpotifyAuthorization(client_id=client_id, client_secret=client_sercet)

    def fetch(self, playlist_id: str, limit: int = 1):
        playlists: Optional[Dict]
        rq = None
        market = os.getenv('SPOTIFY_MARKET')
        try:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            rq = requests.get(
                f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?&limit={limit}&market={market}&fields=artist"
                f"%3Btitle%3Bimages%3Bid%3Bpopularity%3Bname%3Badded_at&",
                headers=headers).json()
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
                    id=str(playlist["track"]["id"]),
                    artist=playlist['track']["album"]["artists"][0]["name"],
                    title=playlist["track"]["id"],
                    cover=[x for x in playlist["track"]["album"]["images"] if x['height'] == 640][0],
                    rank=playlist["track"]["popularity"],
                    album=playlist["track"]["album"]["name"],
                    playlist_id=str(playlist["track"]["album"]["id"]),
                    added_to_playlist=playlist["added_at"],
                    added_by=playlist["added_by"]["id"]
                ))
        self.playlist = songs

    def get_token(self) -> str:
        if self.token.is_active:
            return self.token.token
        self.token.get_token()
        return self.token.token
