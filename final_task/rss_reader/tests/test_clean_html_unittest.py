import unittest
from output_functions import clean_html


class TestCleanHtml(unittest.TestCase):

    def test_cleaning_html(self):
        self.assertEqual(clean_html("<abc>a"), "a", "Should be a")

    def test_not_string(self):
        self.assertRaises(TypeError, clean_html, 52)

    def test_not_zero_string(self):
        self.assertNotEqual(clean_html("<abc>a"), '', "Should be empty")

    def test_zero_string(self):
        self.assertEqual(clean_html("<abc>"), '', "Should be empty")

    def test_normal_tags(self):
        self.assertEqual(clean_html("<abc> Hel </abc>"), ' Hel ', "Should be Hel")


if __name__ == '__main__':
    unittest.main()

