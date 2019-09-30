import unittest

from tests.BaseTestCaseMeme import BaseTestCaseMeme
from utils.meme import NineGag


class TestNineGag(BaseTestCaseMeme):
    def test_parse(self):
        nine = NineGag()
        res = nine._parse("/default/type/hot", 1, 0, "https://9gag.com/v1/group-posts")
        keys = list(res[0].keys())

        self.assertEqual(nine.status_code, 200)
        self.assertEqual(keys[0], "id")
        self.assertIsNone(nine.errors)
        self.assertNotEqual(res, [])

    def test_parse_multiple(self):
        nine = NineGag()
        res = nine._parse("/default/type/hot", self.ar_len_multi)

        self.assertIsNone(nine.errors)
        self.assertEqual(nine._status_code, 200)
        self.assertEqual(len(res), self.ar_len_multi)

    def test_parse_bad_endpoint(self):
        nine = NineGag()
        res = nine._parse(self.string, 1, 0,  "https://9gag.com/v1/group-posts")

        self.assertIsNone(nine.errors)
        self.assertEqual(nine.status_code, 404)
        self.assertEqual(res, [])

    def test_error_int_in_url(self):
        i = f'https://{self.string}'
        nine = NineGag()
        res = nine._parse(i, 1, 0, i)

        self.assertEqual(
            str(nine.errors),
            "Broken endpoint in NineGag module"
        )

    def test_fresh(self):
        nine = NineGag()
        res = nine.fresh(limit=self.ar_len)

        self.assertIsNone(nine.errors)
        self.assertEqual(len(res), self.ar_len)
        self.assertEqual(nine._status_code, 200)

    def test_hot(self):
        nine = NineGag()
        res = nine.hot(limit=3)

        self.assertIsNone(nine.errors)
        self.assertEqual(len(res), 3)
        self.assertEqual(nine.status_code, 200)

    def test_dark_fresh(self):
        nine = NineGag()
        res = nine.dark_fresh(limit=self.ar_len)

        self.assertIsNone(nine.errors)
        self.assertEqual(len(res), self.ar_len)
        self.assertEqual(nine.status_code, 200)

    def test_dark_hot(self):
        nine = NineGag()
        res = nine.dark_hot(limit=3)

        self.assertIsNone(nine.errors)
        self.assertEqual(len(res), 3)
        self.assertEqual(nine.status_code, 200)

    def test_poland_hot(self):
        nine = NineGag()
        res = nine.poland_hot(self.ar_len_multi)

        self.assertIsNone(nine.errors)
        self.assertEqual(len(res), self.ar_len_multi)
        self.assertEqual(nine.status_code, 200)

    def test_poland_fresh(self):
        nine = NineGag()
        res = nine.poland_fresh(2)

        self.assertIsNone(nine.errors)
        self.assertEqual(len(res), 2)
        self.assertEqual(nine.status_code, 200)

    def test_random(self):
        nine = NineGag()
        rand = nine.random()

        keys = list(rand.keys())
        self.assertEqual(nine.status_code, 200)
        self.assertEqual(len(rand), 4)
        self.assertEqual(keys[0], "id")


if __name__ == "__main__":
    unittest.main()
