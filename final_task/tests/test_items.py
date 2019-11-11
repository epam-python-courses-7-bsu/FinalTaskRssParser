import unittest
import items as itms
from feedparser import parse


class TestItems(unittest.TestCase):
    def test_item_to_dict(self):
        item_ = itms.Item('title', 'date', 'link', 'text', ['link1', 'link2'])
        item_dict = {'title': 'title',
                     'date': 'date',
                     'link': 'link',
                     'text': 'text',
                     'image links': ['link1', 'link2']}

        self.assertEqual(itms.item_to_dict(item_), item_dict)

        with self.assertRaises(TypeError):
            itms.item_to_dict(123)

    def test_get_items_from_feedparser(self):
        text_for_parsing = '<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">' \
                           '<channel><title>title0</title><link>link0</link><description>descr</description>' \
                           '<item><title>title1</title><description><p>text1</p></description><link>link1</link>' \
                           '<pubDate>date1</pubDate></item>' \
                           '<item><title>title2</title><description><p>text2</p></description><link>link2</link>' \
                           '<pubDate>date2</pubDate></item>' \
                           '</channel></rss>'
        parser = parse(text_for_parsing)
        items = [itms.Item('title1', 'date1', 'link1', 'text1', []),
                 itms.Item('title2', 'date2', 'link2', 'text2', [])]

        self.assertEqual(itms.get_items_from_feedparser(parser), items)

        with self.assertRaises(TypeError):
            itms.get_items_from_feedparser('abc')


if __name__ == '__main__':
    unittest.main()
