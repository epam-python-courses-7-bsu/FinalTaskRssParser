import unittest
from rss_reader import string_operations


class TestStringOperations(unittest.TestCase):

    def test_readable(self):
        basic_str = '&quot;' + '&comma;' + '&apos;'
        self.assertEqual(string_operations.make_string_readable(basic_str), '\"' + ',' + "\'")

    def test_summary(self):
        basic_str = 'width="130" /></a>bla bla summary bla bla<p><br clear="all" />'
        self.assertEqual(string_operations.extract_topic_info_from_summary(basic_str), "bla bla summary bla bla")


if __name__ == "__main__":
    unittest.main()
