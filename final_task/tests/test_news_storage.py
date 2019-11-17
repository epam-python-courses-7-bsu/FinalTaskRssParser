import unittest
import news_storage
from datetime import datetime
from items import Item, ItemGroup


class TestNewsStorage(unittest.TestCase):
    def setUp(self):
        self.item1 = Item('title1', 'Sat, 16 Nov 2019 19:45:37 -0500', 'link1', 'text1', [])
        self.item2 = Item('title2', 'Sun, 17 Nov 2019 00:30:00 -0500', 'link2', 'text2', [])
        self.item3 = Item('title3', 'Sat, 16 Nov 2019 06:13:25 -0500', 'link3', 'text3', [])
        self.item4 = Item('title4', 'Fri, 15 Nov 2019 10:18:08 -0500', 'link4', 'text4', [])
        self.date = datetime(2019, 11, 16)

    def test_retrieve_news_by_date(self):
        feed = 'feed'
        item_group = ItemGroup(feed, [self.item1, self.item2, self.item3, self.item4])

        extended_item_group = ItemGroup(feed, [self.item1, self.item3])
        extended_limited_item_group = ItemGroup(feed, [self.item1])

        self.assertEqual(news_storage.retrieve_news_by_date(self.date, item_group), extended_item_group)
        self.assertEqual(news_storage
                         .retrieve_news_by_date(self.date, item_group, 1), extended_limited_item_group)

    def test_retrieve_news_by_date_from_list(self):
        feed1 = 'feed1'
        feed2 = 'feed2'
        item_group1 = ItemGroup(feed1, [self.item1, self.item2])
        item_group2 = ItemGroup(feed2, [self.item3, self.item4])

        extended_item_group1 = ItemGroup(feed1, [self.item1])
        extended_item_group2 = ItemGroup(feed2, [self.item3])

        self.assertEqual(news_storage.retrieve_news_by_date_from_list(self.date, [item_group1, item_group2]),
                         [extended_item_group1, extended_item_group2])
        self.assertEqual(news_storage.retrieve_news_by_date_from_list(self.date, [item_group1, item_group2], 1),
                         [extended_item_group1])


if __name__ == '__main__':
    unittest.main()
