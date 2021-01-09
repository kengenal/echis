import requests

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from echis.main import settings
from echis.main.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_MARKET
from echis.modules.token_authorization import SpotifyAuthorization


@dataclass
class Share:
    song_id: str
    title: str
    rank: int
    artist: str
    cover: str
    album: str
    playlist_id: str
    added_to_playlist: str
    added_by: str
    link: str
    api: str


class AbstractShare(ABC):
    playlists: List[Share]

    @abstractmethod
    def fetch(self, playlist_id, limit: int = 1, owner: str = None):
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

    def fetch(self, playlist_id: int, limit: int = 1, owner: Optional[str] = None):
        playlists: Optional[Dict] = {}
        try:
            rq = requests.get(self.url.format(playlist_id)).json()
            if "tracks" in rq:
                playlists = rq["tracks"]["data"]
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
                        link=playlist["link"],
                        api="deezer"
                    ))
            sorted_songs = sorted(songs, key=lambda x: x.added_to_playlist, reverse=True)
            self.playlists = sorted_songs
        except KeyError as err:
            raise Exception(err)
        except Exception:
            raise Exception("Cannot download playlist")

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
        client_id = SPOTIFY_CLIENT_ID
        self.playlists: List[Share] = []
        self.song_url = "https://open.spotify.com/track/{}"
        client_secret = SPOTIFY_CLIENT_SECRET
        self.token = SpotifyAuthorization(client_id=client_id, client_secret=client_secret)
        self.url = "https://api.spotify.com/v1/playlists/{}/tracks?&limit={}&market={" \
                   "}&fields=artist%3Btitle%3Bimages%3Bid%3Bpopularity%3Bname%3Badded_at& "

    def fetch(self, playlist_id: str, limit: int = 1, owner: Optional[str] = None):
        playlists: Optional[Dict] = None
        market = SPOTIFY_MARKET
        try:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            rq = requests.get(self.url.format(playlist_id, limit, market), headers=headers).json()
            if "items" in rq:
                playlists = rq["items"]

            if rq and playlists:
                for playlist in playlists:
                    song_id = str(playlist["track"]["id"])
                    self.playlists.append(Share(
                        song_id=song_id,
                        artist=playlist['track']["album"]["artists"][0]["name"],
                        title=playlist["track"]["name"],
                        cover=[x for x in playlist["track"]["album"]["images"] if x['height'] == 640][0]["url"],
                        rank=playlist["track"]["popularity"],
                        album=playlist["track"]["album"]["name"],
                        playlist_id=str(playlist["track"]["album"]["id"]),
                        added_to_playlist=playlist["added_at"],
                        added_by=playlist["added_by"]["id"],
                        link=self.song_url.format(song_id),
                        api="spotify"
                    ))
        except KeyError:
            raise Exception("Cannot download playlist")
        except Exception:
            raise Exception("Cannot download playlist")

    def playlist_is_exists(self, playlist_id: str):
        try:
            token = self.get_token()
            market_code = SPOTIFY_MARKET
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


class Youtube(AbstractShare, TokenRequired):
    def __init__(self):
        self.playlists: List[Share] = []
        self.open_url = "https://www.youtube.com/watch?v={}"
        self.playlist_url = "https://youtube.googleapis.com/youtube/v3/playlistItems?" \
                            "part=contentDetails&key={}&playlistId={}&maxResults=1"
        self.video_url = "https://www.googleapis.com/youtube/v3/videos?key={}&part=snippet&id={}"

    def fetch(self, playlist_id: str, limit: int = 1, owner: Optional[str] = None):
        playlists: Optional[Dict] = {}
        token = self.get_token()
        try:
            video_id = self.get_video(playlist_id, token)
            rq = requests.get(self.video_url.format(token, video_id)).json()
            if "items" in rq:
                playlists = rq["items"]
            if playlists:
                for playlist in playlists:
                    self.playlists.append(Share(
                        song_id=str(playlist["id"]),
                        title=playlist["snippet"]["title"],
                        rank=0,
                        artist=playlist["snippet"]["title"],
                        cover=playlist["snippet"]["thumbnails"]["high"]["url"],
                        album="Empty on youtube",
                        playlist_id=playlist_id,
                        added_to_playlist=playlist["snippet"]["publishedAt"],
                        added_by=owner,
                        link=self.open_url.format(video_id),
                        api="youtube"
                    ))
        except KeyError:
            raise Exception("Cannot download playlist")
        except Exception:
            raise Exception("Cannot download playlist")

    def get_video(self, playlist_id: str, token: str) -> Optional[str]:
        rq = requests.get(self.playlist_url.format(token, playlist_id))
        if rq.status_code == 200:
            return rq.json()["items"][0]["contentDetails"]["videoId"]
        return None

    def get_token(self) -> str:
        token = settings.YOUTUBE_TOKEN
        if not token:
            raise Exception("Youtube token is empty")
        return token

    def playlist_is_exists(self, playlist_id: str) -> bool:
        try:
            token = self.get_token()
            rq = requests.get(self.playlist_url.format(token, playlist_id))
            if rq.status_code != 200:
                return False
            return True
        except ConnectionError as error:
            raise ConnectionError(error)
