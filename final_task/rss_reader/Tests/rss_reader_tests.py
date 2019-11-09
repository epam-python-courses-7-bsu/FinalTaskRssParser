import unittest
import final_task.rss_reader.rss_reader as reader


class MyTestCase(unittest.TestCase):
    def test_totext(self):
        self.assertEqual(reader.to_text('<div class="test">Test</div>'), 'Test')

    def test_checkurl(self):
        self.assertTrue(reader.check_url(url='https://news.yahoo.com/rss/', verbose=False), True)
        self.assertFalse(reader.check_url(url='https://google.com/', verbose=False), False)

    def test_getfeed(self):
        self.assertIsNotNone(reader.get_feed(url='https://news.yahoo.com/rss/', verbose=False))

    def test_formatfeed(self):
        self.assertIsInstance(reader.format_feed
                              (reader.get_feed(url='https://news.yahoo.com/rss/', verbose=False),
                               verbose=False, limit=1), cls=tuple)


if __name__ == '__main__':
    unittest.main()
