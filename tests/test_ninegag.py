import unittest

from utils.nine_gag import NineGag
from tests.BaseTestCase import BaseTestCase


class TestNineGag(BaseTestCase):
    def test_parse_good(self):
        nine = NineGag()
        res = nine.parse("/default/type/hot", 1)
        keys = list(res[0].keys())

        self.assertEqual(nine.status_code, 200)
        self.assertEqual(keys[0], "id")
        self.assertIsNone(nine.error)
        self.assertNotEqual(res, [])

    def test_parse_multiple(self):
        nine = NineGag()
        res = nine.parse("/default/type/hot", self.ar_len_multi)

        self.assertIsNone(nine.error)
        self.assertEqual(nine.status_code, 200)
        self.assertEqual(len(res), self.ar_len_multi)

    def test_parse_bad_endpoint(self):
        nine = NineGag()
        res = nine.parse(self.string)

        self.assertIsNone(nine.error)
        self.assertEqual(nine.status_code, 404)
        self.assertEqual(res, [])

    def test_parse_bad_connection(self):
        nine = NineGag()
        nine.BASE_URL = self.bad_url
        nine.parse(self.string)
        self.assertEqual(nine.error, "Connection Field, check url")

    def test_error_int_in_url(self):
        i = self.string
        nine = NineGag()
        nine.BASE_URL = i
        res = nine.parse(i, i, i)

        self.assertEqual(
            str(nine.error),
            "Failed to parse url"
        )

    def test_fresh(self):
        nine = NineGag()
        res = nine.fresh(limit=self.ar_len)

        self.assertIsNone(nine.error)
        self.assertEqual(len(res), self.ar_len)
        self.assertEqual(nine.status_code, 200)

    def test_hot(self):
        nine = NineGag()
        res = nine.hot(limit=self.ar_len)

        self.assertIsNone(nine.error)
        self.assertEqual(len(res), self.ar_len)
        self.assertEqual(nine.status_code, 200)

    def test_dark_fresh(self):
        nine = NineGag()
        res = nine.dark_fresh(self.ar_len)

        self.assertIsNone(nine.error)
        self.assertEqual(len(res), self.ar_len)
        self.assertEqual(nine.status_code, 200)

    def test_dark_hot(self):
        nine = NineGag()
        res = nine.dark_hot(self.ar_len_multi)

        self.assertIsNone(nine.error)
        self.assertEqual(len(res), self.ar_len_multi)
        self.assertEqual(nine.status_code, 200)

    def test_poland_hot(self):
        nine = NineGag()
        res = nine.poland_hot(self.ar_len_multi)

        self.assertIsNone(nine.error)
        self.assertEqual(len(res), self.ar_len_multi)
        self.assertEqual(nine.status_code, 200)

    def test_poland_fresh(self):
        nine = NineGag()
        res = nine.poland_fresh(self.ar_len_multi)

        self.assertIsNone(nine.error)
        self.assertEqual(len(res), self.ar_len_multi)
        self.assertEqual(nine.status_code, 200)

    def test_random(self):
        nine = NineGag()
        rand = nine.random()

        keys = list(rand.keys())
        self.assertEqual(nine.status_code, 200)
        self.assertEqual(len(rand), 4)
        self.assertEqual(keys[0], "id")

    def test_random_exeption(self):
        nine = NineGag()
        nine.RANDOM_URL = self.string
        rand = nine.random()

        self.assertEqual(rand, "Cannot get random meme")
        self.assertEqual(nine.status_code, 500)


if __name__ == "__main__":
    unittest.main()
