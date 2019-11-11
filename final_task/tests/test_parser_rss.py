import unittest
import parser_rss


class TestParserRss(unittest.TestCase):
    def test_create_feedparser(self):
        with self.assertRaises(Exception):
            parser_rss.create_feedparser('abcdefg')

    def test_format_description(self):
        descr = '<description><p><img src="source" width="130" height="86" alt="name of image" border="0" >' \
                'text<p><br clear="all"></description>'

        self.assertEqual(parser_rss.format_description(descr), ('[image 1: name of image][1]text', ['source']))

        with self.assertRaises(TypeError):
            parser_rss.format_description(123)


if __name__ == '__main__':
    unittest.main()
