import requests


class Meme:
    URL = 'https://www.reddit.com/r/memes/random.json'

    def run(self):
        r = requests.get(self.URL, headers={'User-agent': 'your bot 0.1'})
        data = r.json()
        json_clear = data[0]['data']['children'][0]['data']
        data = json_clear
        array = {"title": data['title'], "image": data['url']}

        return array


if __name__ == '__main__':
    Meme()
