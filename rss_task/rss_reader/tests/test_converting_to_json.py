import unittest
from output_functions import converting_to_json
from Classes.novelty import Novelty


class ConvertJson(unittest.TestCase):
    def test_converting_if_novelty(self):
        pack_of_news = [Novelty(1, "AAA", '12:04:2020', 'Bla-bla-bla', 'abcdefgh', 'link', 'alt_text', '20200412', 'a')]
        self.assertTrue(converting_to_json(pack_of_news))

    def test_converting_if_integers(self):
        pack_of_news = [Novelty(1, "AAA", '12:04:2020', 'Bla-bla-bla', 'abcdefgh', 123, 'alt_text', 20200412, 'a')]
        self.assertRaises(TypeError, converting_to_json(pack_of_news))

    def test_converting_if_none(self):
        pack_of_news = [Novelty(None, "AAA", '12:04:2020', 'Bla-bla-bla', 'abcdefgh', '123', 'alt_text', '20212', 'a')]
        self.assertRaises(TypeError, converting_to_json(pack_of_news))


if __name__ == '__main__':
    unittest.main()
