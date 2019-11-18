from final_task.rss_reader.scripts.News import *
import unittest
from dateutil import parser


class TestNews(unittest.TestCase):

    def setUp(self):
        self.item = News(feed="feed",
                         title="title",
                         date=parser.parse("2019-11-17 10:44:20-05:00"),
                         link="link",
                         info_about_image="info_about_image",
                         briefly_about_news="briefly_about_news",
                         links_from_news=["link", "link_on_image"]
                         )

    def test_str(self):
        self.assertTrue(str(self.item) == "Feed: feed\n"
                                          "Title: title \n"
                                          "Date: 2019-11-17 10:44:20-05:00 \n"
                                          "Link: link\n"
                                          "Info about image: info_about_image\n"
                                          "Briefly about news: briefly_about_news\n"
                                          "Links: \n"
                                          "[0] link\n"
                                          "[1] link_on_image\n")

    def test_get_json(self):
        data = self.item.get_json()
        self.assertEqual(data['Feed'], 'feed')
        self.assertEqual(data['Title'], 'title')
        self.assertEqual(data['Date'], '2019-11-17 10:44:20-05:00')
        self.assertEqual(data['Link'], 'link')
        self.assertEqual(data['Info about image'], 'info_about_image')
        self.assertEqual(data['Briefly about news'], 'briefly_about_news')
        self.assertEqual(data['Links'], ['link', 'link_on_image'])