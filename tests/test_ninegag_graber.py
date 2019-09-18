import unittest
import sys
import os
import random

from utils.nine_gag import NineGagGrab
from tests.BaseTestCase import BaseTestCase



class TestNineGagGrabe(BaseTestCase):
    def test_get_id_good_link(self):
        nine = NineGagGrab()
        id = nine.get_id(self.link)

        self.assertEqual(len(id), 7)

    def test_get_id_broke_link(self):
        nine = NineGagGrab()
        id = nine.get_id(self.broke_link)

        self.assertEqual("""
            This link is not supported, take link to post,
            like this https://9gag.com/gag/aXY5qvg
        """, id)

    def test_grab_meme(self):
        nine = NineGagGrab()
        mem = nine.grab_meme(self.meme_id)

        self.assertEqual(mem['id'], 'axz6oYK')
        self.assertEqual(
            mem['url'],
            'https://img-9gag-fun.9cache.com/photo/axz6oYK_460svvp9.webm'
        )
        self.assertEqual(mem['title'], 'A freaking plasma rifle. ')

    def test_grab_meme_gif(self):
        nine = NineGagGrab()
        mem = nine.grab_meme(self.meme_id)

        self.assertEqual(mem['id'], 'axz6oYK')
        self.assertEqual(mem['type'], 'Animations')

    def test_grab_meme_photo(self):
        nine = NineGagGrab()
        mem = nine.grab_meme(self.meme_id_photo)

        self.assertEqual(mem['type'], 'Photo')

    def test_status_code(self):
        nine = NineGagGrab()
        mem = nine.grab_meme(self.meme_id)

        self.assertEqual(nine.status_code, 200)

    def test_grab_meme(self):
        nine = NineGagGrab()
        mem = nine.grab_meme(self.string)

        self.assertEqual(mem, "Meme not found")
        self.assertEqual(nine.status_code, 404)


if __name__ == '__main__':
    unittest.main()
