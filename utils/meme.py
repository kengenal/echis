import re
from urllib.parse import urlparse

import requests


class NineGag:
    _BASE_URL = "https://9gag.com/v1/group-posts"
    _RANDOM_URL = "http://bit.ly/3231YVs"
    _status_code = None
    _error = None
    _global_hot = '/group/default/type/hot'
    _global_fresh = ""
    _dark_humor_hot = "/group/darkhumor/type/hot"
    _dark_humor_fresh = ""
    _poland_fresh_url = "/group/poland/type/fresh"
    _poland_hot_url = "/group/poland/type/hot"
    _endpoint = None

    def _parse(self, what: str = None, limit: int = 1, rang: int = 0, endpoint: str = _BASE_URL):
        images_type = ["Article", "Photo", "Photo", "FPhoto"]
        try:
            payloads = {
                "c": str(rang)
            }
            req = requests.get(url=endpoint + what, params=payloads)
            self._endpoint = req.url
            self._status_code = req.status_code
            res = []
            if req.status_code == 200:
                r = req.json()["data"]["posts"]
                for i in range(0, limit):
                    if r[i]["type"] in images_type:
                        r[i]["type"] = "image"
                        position = "image460"
                    else:
                        position = "image460sv"
                        r[i]["type"] = "gif"
                    res.append({
                        "id": r[i]["id"],
                        "title": r[i]["title"],
                        "url": r[i]["images"][position]["url"],
                        "type": r[i]["type"],
                        "points": r[i]["upVoteCount"],
                    })
                return res[:limit]
            else:
                return []
        except Exception as error:
            self._status_code = 500
            self._error = "Broken endpoint in NineGag module"
            return [error]

    def fresh(self, limit: int = 10, rang: int = 0):
        return self._parse(what=self._global_fresh, limit=limit, rang=rang, endpoint=self._BASE_URL)

    def hot(self, limit: int = 10, rang: int = 0):
        return self._parse(what=self._global_hot, limit=limit, rang=rang, endpoint=self._BASE_URL)

    def dark_fresh(self, limit: int = 10, rang: int = 0):
        return self._parse(what=self._dark_humor_fresh, limit=limit, rang=rang, endpoint=self._BASE_URL)

    def dark_hot(self, limit: int = 10, rang: int = 0):
        return self._parse(what=self._dark_humor_hot, limit=limit, rang=rang, endpoint=self._BASE_URL)

    def poland_hot(self, limit: int = 10, rang: int = 0):
        return self._parse(what=self._poland_hot_url, limit=limit, rang=rang, endpoint=self._BASE_URL)

    def poland_fresh(self, limit: int = 10, rang: int = 0):
        return self._parse(what=self._poland_fresh_url, limit=limit, rang=rang, endpoint=self._BASE_URL)

    def random(self):
        nine = NineGagGrab()
        try:
            r = requests.get(self._RANDOM_URL, allow_redirects=True)
            self._status_code = r.status_code
            if r.status_code == 200:
                id = nine.get_id(r.url)
                data = nine.grab_meme(id)
                self._status_code = nine.status_code
                return data
            else:
                self._error = "Cannot get random meme"
                return []
        except Exception as error:
            self._status_code = 500
            self._error = [error]
            return "Cannot get random meme"

    @property
    def errors(self):
        return self._error

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def status_code(self):
        return self._status_code


class NineGagGrab:
    _status_code = None
    _IMAGE = "_700b.jpg"
    _GIF = "_460svvp9.webm"
    _GAG_URL = "https://img-9gag-fun.9cache.com/photo/"

    def get_id(self, url: str):
        url_parse = urlparse(url)
        id = str(url.split("/")[-1])
        if url_parse.netloc == '9gag.com' and len(id) == 7:
            return id
        else:
            return """
            This link is not supported, take link to post,
            like this https://9gag.com/gag/aXY5qvg
        """

    def grab_meme(self, id: str):
        params = dict()
        params["id"] = id
        if requests.get(self._GAG_URL + id + self._GIF).ok:
            self._status_code = 200
            params['type'] = 'gif'
            params["image_url"] = self._GAG_URL + id + self._GIF
        elif requests.get(self._GAG_URL + id + self._IMAGE).ok:
            self._status_code = 200
            params["type"] = "image"
            params["image_url"] = self._GAG_URL + id + self._GIF
        else:
            self._status_code = 404
            params["Error"] = "Meme not found"
            params["_status_code"] = self._status_code
        if self._status_code == 200:
            params['url'] = "https://9gag.com/gag/" + id
            r = requests.get("https://9gag.com/gag/" + id).text
            regexp = re.search(
                '(?<=<title>).+?(?=</title>)',
                r,
                re.DOTALL
            ).group().strip()
            params["title"] = regexp.split('-')[0]
            return params
        else:
            return "Meme not found"

    @property
    def status_code(self):
        return self._status_code


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
            if query is not 'random':
                payloads["q"] = query
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
