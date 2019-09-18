import requests
import shutil
import re

from urllib.parse import urlparse
from requests.exceptions import ConnectionError


class NineGag:
    BASE_URL = "https://9gag.com/v1/group-posts"
    RANDOM_URL = "http://bit.ly/3231YVs"
    status_code = None
    error = None
    global_hot = '/group/default/type/hot'
    global_fresh = ""
    dark_humor_hot = "/group/darkhumor/type/hot"
    dark_humor_fresh = ""
    poland_fresh_url = "/group/poland/type/fresh"
    poland_hot_url = "/group/poland/type/hot"

    def parse(self, what: str = "", limit: int = 10, rang: int = 0):
        try:
            req = requests.get(self.BASE_URL + what + "?c=" + str(rang))
            self.status_code = req.status_code
            res = list()
            if req.status_code == 200:
                r = req.json()["data"]["posts"]
                for i in range(0, limit):
                    if r[i]["type"] == "Photo":
                        position = "image460"
                    else:
                        position = "image460sv"
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
        except ConnectionError as e:
            self.error = "Connection Field, check url"
            return []
        except Exception as e:
            self.error = "Failed to parse url"
            return []

    def fresh(self, limit: int = 10, rang: int = 0):
        data = self.parse(self.global_fresh, limit, rang)
        return data

    def hot(self, limit: int = 10, rang: int = 0):
        data = self.parse(self.global_hot, limit, rang)
        return data

    def dark_fresh(self, limit: int = 10, rang: int = 0):
        data = self.parse(self.dark_humor_fresh, limit, rang)
        return data

    def dark_hot(self, limit: int = 10, rang: int = 0):
        data = self.parse(self.dark_humor_hot, limit, rang)
        return data

    def poland_hot(self, limit: int = 10, rang: int = 0):
        data = self.parse(self.poland_hot_url, limit, rang)
        return data

    def poland_fresh(self, limit: int = 10, rang: int = 0):
        data = self.parse(self.poland_fresh_url, limit, rang)
        return data

    def random(self):
        nine = NineGagGrab()
        try:
            r = requests.get(self.RANDOM_URL, allow_redirects=True)
            self.status_code = r.status_code
            id = nine.get_id(r.url)
            data = nine.grab_meme(id)
            self.status_code = nine.status_code
            return data
        except Exception as error:
            self.status_code = 500
            self.error = error
            return "Cannot get random meme"


class NineGagGrab:
    status_code = None
    IMAGE = "_700b.jpg"
    GIF = "_460svvp9.webm"
    GAG_URL = "https://img-9gag-fun.9cache.com/photo/"

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
        params = {}
        params["id"] = id
        if requests.get(self.GAG_URL + id + self.GIF).ok:
            self.status_code = 200
            params['type'] = 'Animations'
            params["url"] = self.GAG_URL + id + self.GIF
        elif requests.get(self.GAG_URL + id + self.IMAGE).ok:
            self.status_code = 200
            params["type"] = "Photo"
            params["url"] = self.GAG_URL + id + self.GIF
        else:
            self.status_code = 404
            params["Error"] = "Meme not found"
            params["status_code"] = self.status_code
        if self.status_code == 200:
            r = requests.get("https://9gag.com/gag/" + id).text
            reexp = re.search(
                '(?<=<title>).+?(?=</title>)',
                r,
                re.DOTALL
            ).group().strip()
            params["title"] = reexp.split('-')[0]
            return params
        else:
            return "Meme not found"
