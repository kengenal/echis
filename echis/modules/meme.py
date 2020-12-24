from typing import Dict, List

import requests


class RedditMeme:
    RED_ENDPOINT = "https://www.reddit.com/r/memes/search.json"
    RANDOM_ENDPOINT = "https://www.reddit.com/r/memes/random.json"
    status_code = None

    def _parse(self, query: str = None, limit: int = 1, sort: str = None, endpoint: str = None) -> List[Dict]:
        try:
            headers = {
                'User-agent': 'your bot 0.1'
            }
            payload = {
                "limit": limit,
                "sort": sort
            }
            if query != 'random':
                payload["q"] = query.replace("-", "_").strip()
            res = self.query(endpoint=endpoint, headers=headers, payload=payload)
            data = []
            if res:
                for i in res:
                    data.append({
                        "title": i["data"]["title"],
                        "url": i["data"]["url"],
                        "score": i["data"]["score"],
                        "author": i["data"]["author_fullname"],
                        "type": i["data"]["post_hint"]
                    })
                return data[:limit] if len(data) > 0 else [{}]
        except Exception as error:
            print(error)
            raise Exception("Problem with downloading meme")

    def query(self, endpoint: str, headers: Dict, payload: Dict) -> List[Dict]:
        r = requests.get(url=endpoint, headers=headers, params=payload)
        self.status_code = r.status_code
        if r.status_code == 200:
            res = r.json()["data"]["children"] if "data" in r.json() else r.json()[0]["data"]["children"]
            return res
        return [{}]

    @property
    def hot(self, query: str = "dark humor", limit: int = 1):
        return self._parse(query=query, limit=limit, sort="hot", endpoint=self.RED_ENDPOINT)

    @property
    def fresh(self, query: str = "dark humor", limit: int = 1):
        return self._parse(query=query, limit=limit, sort="new", endpoint=self.RED_ENDPOINT)

    @property
    def random(self, limit: int = 1):
        return self._parse(query="random", limit=limit, sort="random", endpoint=self.RANDOM_ENDPOINT)

    def by_query(self, query: str = "", limit: int = 1):
        return self._parse(query=query, limit=limit, sort="", endpoint=self.RED_ENDPOINT)
