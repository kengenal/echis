import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import configparser

import unittest
from Youtube import YoutubeSearch

class YoutubeTest(unittest.TestCase):
    def setUp(self):
        cnf = configparser.ConfigParser()
        cnf.read('../cnf.ini')
        cnf.sections()
        self.key = cnf["TOKENS"]["youtube_api"]
        self.url = cnf["URLS"]["youtube_search"]
        self.youtube = YoutubeSearch()

    def test_search_good_token_getall(self):
        self.youtube.token(self.key)
        self.youtube.search("metallica", self.url)
        all = self.youtube.get_all()
        self.assertEqual(all["status"], 200)
        self.assertIsNotNone(all["id"])

    def test_search_getters_good_token(self):
        self.youtube.token(self.key)
        self.youtube.search("metallica", self.url)
        id, status = self.youtube.get_id, self.youtube.status
        self.assertEqual(status, 200)
        self.assertIsNotNone(id)
        
    def test_search_empty_token(self):
        yt = Youtube()
        res = yt.token(" ")
        self.assertIsNone(res)
        self.assertEqual(yt.get_errors(), None)
    
    def test_search_bad_token(self):
        yt = Youtube()
        res = yt.token("randomstring")
        response = yt.search("metallica", self.url)
        self.assertIsNone(response)
        self.assertEqual(yt.get_errors(), "Request error, check token or query string")

    def test_get_url(self):
        self.youtube.token(self.key)
        self.youtube.search("metallica", self.url)
        url = self.youtube.get_url()
        self.assertIsNotNone(url)


if __name__ == '__main__':
    unittest.main()
