import unittest
import os

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.link = 'https://9gag.com/gag/axz6oYK'
        self.meme_id_photo = "aNY6654"
        self.broke_link = 'https://9gagel.com/gag/12'
        self.names = 'what-the-hell'
        self.meme_id = 'axz6oYK'
        self.ar_len = 3
        self.ar_len_multi = 10
        self.string = "RandomString"
        self.bad_url = "https://HelloWorld"
        self.gif = "https://img-9gag-fun.9cache.com/photo/amBEP14_460sv.mp4"
        self.image = "https://img-9gag-fun.9cache.com/photo/amBEgWX_700b.jpg"


    def is_exists(self, path):
        what = os.path.isfile(path)
        os.remove(path)
        return what
