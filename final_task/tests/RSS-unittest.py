import unittest
import sys
sys.path.append('../')
from rss_reader.rss_reader import RSSReader, arg_parse

RSS_DICT_TEST = {
    'updated': 'Fri, 08 Nov 2019 13:59:06 GMT',
    'href': 'https://news.yahoo.com/rss',
    'feed': {'title': 'Yahoo News - Latest News & Headlines'},
    'bozo': 0,
    'status': 200,
    'version': 'rss20',
    'etag': '"c3e4279c4a667ef345dcb64d5344199b"',
    'encoding': 'utf-8',
    'entries': [
        {
            'title': 'Graham now says Trump',
            'published': 'Wed, 06 Nov 2019 14:22:10 -0500',
            'id': 'graham-trump-ukraine-incoherent-quid-pro-quo-192210175.html',
            'summary': '<p><a href="test"><img src="test2" alt="Trump" title="Trump"></a>day<p><br clear="all">',
            'link': 'https://news.yahoo.com/graham-trump-ukraine.html'
        },
        {
            'title': '2 escaped murder suspects arrested at US-Mexico border',
            'published': 'Thu, 07 Nov 2019 07:25:46 -0500',
            'id': '2-escaped-murder-suspects-arrested-050940220.html',
            'summary': '<p><a href="test3"><img src="test4" alt="border" title="border"></a>are<p><br clear="all">',
            'link': 'https://news.yahoo.com/2-escaped-murder-suspects-arrested.html'
        },
    ],
}


class RSSTestCase(unittest.TestCase):
    def setUp(self):
        self.rss = RSSReader('')

    def test_make_news_data(self):
        result = self.rss.make_news_data(RSS_DICT_TEST['entries'][0])
        self.assertEqual(result.get('Title'), 'Graham now says Trump')
        self.assertEqual(result.get('Date'), 'Wed, 06 Nov 2019 14:22:10 -0500')
        self.assertEqual(result.get('Summary'), 'day')
        self.assertEqual(result.get('Link'), 'https://news.yahoo.com/graham-trump-ukraine.html')
        self.assertEqual(result.get('Image'), 'Trump\nSource of image: test2')

    def test_information_about_site(self):
        result = self.rss.information_about_site(RSS_DICT_TEST)
        self.assertEqual(result.get('Feed'), 'Yahoo News - Latest News & Headlines')
        self.assertEqual(result.get('Updated'), 'Fri, 08 Nov 2019 13:59:06 GMT')
        self.assertEqual(result.get('Version'), 'rss20')

    def test_news_data_collection(self):
        result = self.rss.news_data_collection(RSS_DICT_TEST)
        self.assertEqual(result[0].get('Title'), 'Graham now says Trump')
        self.assertEqual(result[0].get('Date'), 'Wed, 06 Nov 2019 14:22:10 -0500')
        self.assertEqual(result[0].get('Summary'), 'day')
        self.assertEqual(result[0].get('Link'), 'https://news.yahoo.com/graham-trump-ukraine.html')
        self.assertEqual(result[0].get('Image'), 'Trump\nSource of image: test2')
        self.assertEqual(result[1].get('Title'), '2 escaped murder suspects arrested at US-Mexico border')
        self.assertEqual(result[1].get('Date'), 'Thu, 07 Nov 2019 07:25:46 -0500')
        self.assertEqual(result[1].get('Summary'), 'are')
        self.assertEqual(result[1].get('Link'), 'https://news.yahoo.com/2-escaped-murder-suspects-arrested.html')
        self.assertEqual(result[1].get('Image'), 'border\nSource of image: test4')

    def test_arg_parse(self):
        parser = arg_parse(['source', '--limit', '1', '--json', '--verbose', '--version'])
        self.assertTrue(parser.limit == 1)
        self.assertTrue(parser.source == 'source')
        self.assertTrue(parser.json)
        self.assertTrue(parser.verbose)
        self.assertTrue(parser.version)


if __name__ == '__main__':
    unittest.main()
