import unittest
import parser_rss
from exceptions import GettingRSSException


class TestParserRss(unittest.TestCase):
    def test_create_feedparser(self):
        with self.assertRaises(GettingRSSException):
            parser_rss.create_feedparser('abcdefg')

    def test_format_description(self):
        descr1 = '<description><p><img src="source" width="130" height="86" alt="name of image" border="0" >' \
                'text<p><br clear="all"></description>'
        descr2 = descr1.replace('source', '')

        self.assertEqual(parser_rss.format_description(descr1), ('[image 1: name of image][1]text', ['source']))
        self.assertEqual(parser_rss.format_description(descr2), ('text', []))

        with self.assertRaises(TypeError):
            parser_rss.format_description(123)


if __name__ == '__main__':
    unittest.main()
