from rss_reader import find_news, collect_news, find_channel
from CustomException import WrongUrl
import unittest


class TestNews(unittest.TestCase):
    def test_find(self):
        self.assertNotEqual(find_news('https://lenta.ru/rss'), None)
        self.assertNotEqual(find_news('https://news.yahoo.com/rss/world'), None)
        self.assertNotEqual(find_news('https://news.tut.by/rss/economics.rss'), None)
        self.assertNotEqual(find_news('https://auto.onliner.by/feed'), None)
        self.assertEqual(find_news('https://www.google.ru/'), [])
        self.assertEqual(find_news('https://vk.com/'), [])
        self.assertRaises(WrongUrl, find_news, 'random_text')

    def test_collect(self):
        items1 = find_news('https://lenta.ru/rss')
        self.assertNotEqual(collect_news(items1, 3), [])
        items2 = find_news('https://auto.onliner.by/feed')
        self.assertNotEqual(collect_news(items2, 3), [])
        items3 = find_news('https://www.google.ru/')
        self.assertEqual(collect_news(items3, 3), [])

    def test_channel(self):
        self.assertNotEqual(find_channel('https://lenta.ru/rss'), [])
        self.assertNotEqual(find_channel('https://news.yahoo.com/rss/world'), [])
        self.assertNotEqual(find_channel('https://news.tut.by/rss/economics.rss'), [])
        self.assertEqual(find_channel('https://www.google.ru/'), None)
        self.assertEqual(find_channel('https://vk.com/'), None)