import requests
import configparser
import sys
import youtube_dl
import discord

from urllib.parse import urlparse

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YoutubeSearch:
    id = None
    token = None
    status = None
    errors = None
    url = None

    def token(self, token):
        if token is not None and token:
            self.token = token
        else:
            self.errors = "Token is empty"
            return None

    def search(self, query, url):
        if self.token is not None and url:
            payloads = f"?part=id&type=video&maxResults=1&key={self.token}&q={query}"
            full_url = url + payloads
            try:
                r = requests.get(full_url)
            except:
                self.errors =  "Request error, check token or query string"
                return None
            if r.status_code == 200:
                data = r.json()
                self.id = data['items'][0]['id']['videoId']
                self.status = r.status_code
                self.url = f"https://www.youtube.com/watch?v={self.id}"
            else:
                self.errors = "Request error, check token or query string"
        else:
            self.errors = "Token is empty or url"
            return None
    
    @property
    def get_all(self):
        return {"status": self.status, "id": self.id}

    @property
    def get_id(self):
        return self.id

    @property
    def get_status(self):
        return self.status

    @property
    def get_errors(self):
        return self.errors
    
    @property
    def get_url(self):
        return self.url
    


class YoutubeStream(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def is_url(query):
    u = True
    try:
        url = urlparse(query)
        if url.hostname:
            u = True
    except Exception as error:
        u = False
    return u