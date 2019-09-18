import requests
import sys


class Meme:
    url = None
    image = None
    title = None
    status = None

    def __init__(self, url):
        if url is not None:
            self.url = url
        else:
            self.url = None

    def run(self):
        if self.url is None:
            return "Url not found"
        try:
            r = requests.get(self.url, headers={'User-agent': 'your bot 0.1'})
        except:
            return "Request fail, check url"
            sys.exit()
        if r.status_code == 200:
            data = r.json()
            json_clear = data[0]['data']['children'][0]['data']
            data = json_clear
            self.image, self.title, self.status = data['url'], data['title'], r.status_code
            return {"status": r.status_code}
        else:
            return {"status": r.status_code}

    @property
    def get_all(self):
        return {"title": self.title, "image": self.image, "status": self.status}

    @property
    def get_title(self):
        return self.title

    @property
    def get_image_url(self):
        return self.image

    @property
    def get_status(self):
        return self.status
