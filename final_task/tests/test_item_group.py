import unittest
from item import Item
from feedparser import parse
import item_group


class TestItems(unittest.TestCase):
    def setUp(self):
        items = [Item('title1', 'date1', 'link1', '[image 1: alt1][1]text1', ['img1']),
                 Item('title2', 'date2', 'link2', 'text2', []),
                 Item('title3', 'date3', 'link3', 'text3', [])]
        item_gr = item_group.ItemGroup('title0', items)

        self.item_gr = item_gr

    def test_get_item_group_from_feedparser(self):
        text_for_parsing = '<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">' \
                           '<channel><title>title0</title><link>link0</link><description>descr</description>' \
                           '<item><title>title2</title><description><p>text2</p></description>' \
                           '<link>link2</link><pubDate>date2</pubDate></item>' \
                           '<item><title>title3</title><description><p>text3</p></description><link>link3</link>' \
                           '<pubDate>date3</pubDate></item></channel></rss>'

        parser = parse(text_for_parsing)
        self.item_gr.items = self.item_gr.items[1:]

        self.assertEqual(item_group.get_item_group_from_feedparser(parser), self.item_gr)

    def test_item_group_as_str(self):
        expected_str = 'Feed: title0\n' \
                       '\nTitle: title1' \
                       '\nDate: date1' \
                       '\nLink: link1' \
                       '\nText: [image 1: alt1][1]text1' \
                       '\nImage links:\n\t[1]: [img1]\n' \
                       '\nTitle: title2' \
                       '\nDate: date2' \
                       '\nLink: link2' \
                       '\nText: text2\n\n'
        self.item_gr.items = self.item_gr.items[:2]

        self.assertEqual(str(self.item_gr), expected_str)


if __name__ == '__main__':
    unittest.main()
