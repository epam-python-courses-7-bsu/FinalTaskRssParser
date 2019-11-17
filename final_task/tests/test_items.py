import unittest
import items as itms
from feedparser import parse


class TestItems(unittest.TestCase):
    def test_get_item_group_from_feedparser(self):
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
        item_group = itms.ItemGroup('title0', items)

        self.assertEqual(itms.get_item_group_from_feedparser(parser), item_group)

        with self.assertRaises(TypeError):
            itms.get_item_group_from_feedparser('abc')


if __name__ == '__main__':
    unittest.main()
