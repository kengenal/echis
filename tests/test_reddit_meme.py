import os
import unittest
from utils.meme import RedditMeme


class TestRedMemes(unittest.TestCase):
    def setUp(self):
        self.endpoint_reddit = "https://www.reddit.com/r/memes/search.json"

    def test_parse(self):
        red = RedditMeme()
        parse = red._parse(query="dark meme",
                           limit=1,
                           sort="hot",
                           endpoint=self.endpoint_reddit)

        self.assertNotEqual(parse[0]["title"], [])
        self.assertNotEqual(parse[0]["url"], [])

    def test_parse_error(self):
        red = RedditMeme()
        parse = red._parse(query="",
                           limit=1,
                           sort="osime",
                           endpoint=self.endpoint_reddit)

        self.assertIsNotNone(red.error)
        self.assertNotEqual(red.status_code, "404")
        self.assertEquals(red.error, "Not found")
        self.assertEquals(parse, [])

    def test_parse_connection_error(self):
        red = RedditMeme()
        parse = red._parse(query="dark humor",
                           limit=1,
                           sort="hot",
                           endpoint="https://random-string")

        self.assertIsNotNone(red.error)
        self.assertNotEqual(red.status_code, "500")
        self.assertIsNotNone(red.error)
        self.assertEquals(parse, [])



if __name__ == "__main__":
    unittest.main()
