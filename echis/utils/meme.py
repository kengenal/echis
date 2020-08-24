import re
from urllib.parse import urlparse

import requests


class RedditMeme:
    _RED_ENDPOINT = "https://www.reddit.com/r/memes/search.json"
    _RANDOM_ENDPOINT = "https://www.reddit.com/r/memes/random.json"
    _error = None
    _status_code = None
    _endpoint = None

    def _parse(self, query: str = None, limit: int = 1, sort: str = None, endpoint: str = None):
        try:
            headers = {
                'User-agent': 'your bot 0.1'
            }
            payloads = {
                "limit": limit,
                "sort": sort
            }
            if query != 'random':
                payloads["q"] = query.replace("-", "_").strip()
            r = requests.get(url=endpoint, headers=headers, params=payloads)
            self._endpoint = r.url
            res = r.json()["data"]["children"] if "data" in r.json() else r.json()[0]["data"]["children"]
            data = []
            if r.status_code == 200 and res:
                self._status_code = r
                for i in res:
                    data.append({
                        "title": i["data"]["title"],
                        "url": i["data"]["url"],
                        "score": i["data"]["score"],
                        "author": i["data"]["author_fullname"],
                        "type": i["data"]["post_hint"]
                    })
                return data[:limit]
            elif r.status_code == 200 and not res:
                self._status_code = 404
                self._error = "Not found"
                return []
            else:
                self._status_code = r.status_code
                self._error = "Query not found"
                return []
        except Exception as error:
            self._status_code = 500
            self._error = error
            return []

    def hot(self, query: str = "dark humor", limit: int = 1):
        return self._parse(query=query, limit=limit, sort="hot", endpoint=self._RED_ENDPOINT)

    def fresh(self, query: str = "dark humor", limit: int = 1):
        return self._parse(query=query, limit=limit, sort="new", endpoint=self._RED_ENDPOINT)

    def random(self, limit: int = 1):
        return self._parse(query="random", limit=limit, sort="random", endpoint=self._RANDOM_ENDPOINT)

    def query(self, query: str="", limit: int=1):
        return self._parse(query=query, limit=limit, sort="", endpoint=self._RED_ENDPOINT)

    @property
    def error(self):
        return self._error

    @property
    def status_code(self):
        return self._status_code

    @property
    def endpoint(self):
        return self._endpoint
