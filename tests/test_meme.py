import sys
import os
#sys.path.insert(0, os.path.abspath('..'))

import unittest
from src.lib.Meme import Meme

class MemeTest(unittest.TestCase):
    def setUp(self):
        good_url = "https://www.reddit.com/r/memes/random.json"
        bad_url = "http://Random---String"
        self.meme_ini = Meme(good_url)
        self.bad_ini = Meme(bad_url)

    def test_get_all_good_url(self):
        self.meme_ini.run()
        all_memes = self.meme_ini.get_all()
        self.assertEqual(all_memes["status"], 200)
        self.assertIsNotNone(all_memes["image"])
        self.assertIsNotNone(all_memes["title"])

    def test_get_all_bad_url(self):
        self.bad_ini.run()
        all_memes = self.bad_ini.get_all()
        self.assertNotEqual(all_memes["status"], 200)
        self.assertIsNone(all_memes["image"])
        self.assertIsNone(all_memes["title"])

    def test_getters_good_url(self):
        self.meme_ini.run()
        title = self.meme_ini.get_title()
        image = self.meme_ini.get_image_url()
        status = self.meme_ini.get_status()
        self.assertEqual(status, 200)
        self.assertIsNotNone(image)
        self.assertIsNotNone(title)

    def test_getters_bad_url(self):
        self.bad_ini.run()
        title = self.bad_ini.get_title()
        image = self.bad_ini.get_image_url()
        status = self.bad_ini.get_status()
        self.assertNotEqual(status, 200)
        self.assertIsNone(image)
        self.assertIsNone(title)

if __name__ == '__main__':
    unittest.main()
