import os
import sys

sys.path.insert(1, 'final_task/rss_reader')
from parser_rss import *
from News import News
import unittest
import feedparser


class TestParserRss(unittest.TestCase):

    def setUp(self):
        self.summary = '''<p><a href="https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html">\
<img src="http://l1.yimg.com/uu/api/res/1.2/IKBjTl0jeU0BCnrjqbCKAw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https:\
//media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/440e0010-0714-11ea-9bcb-45ff7f6277b3" \
width="130" height="86" alt="NATO ally expels undercover Russian spy " align="left" title="NATO ally expels undercover\
 Russian spy " border="0" ></a>In a rare move,NATO ally Bulgaria has expelled an undercover spy affiliated with \
the Russian military intelligence service, according to a Western intelligence source.<p><br clear="all">'''
        self.item = News(feed="feed",
                         title="title",
                         date=parser.parse("2019-11-17 10:44:20-05:00"),
                         link="link",
                         info_about_image="info_about_image",
                         briefly_about_news="briefly_about_news",
                         links_from_news=["link", "link_on_image"]
                         )
        self.result = "1\n"
        self.result += "Feed: feed\n"
        self.result += "Title: title \n"
        self.result += "Date: 2019-11-17 10:44:20-05:00 \n"
        self.result += "Link: link\n"
        self.result += "Info about image: info_about_image\n"
        self.result += "Briefly about news: briefly_about_news\n"
        self.result += "Links: \n"
        self.result += "[0] link\n"
        self.result += "[1] link_on_image\n"
        self.result += '\n'
        self.result += '-' * 100

        if os.path.isfile('final_task/tests/news_feed_for_test.xml'):
            self.url = 'final_task/tests/news_feed_for_test.xml'
        else:
            self.url = 'news_feed_for_test.xml'

        self.news_feed = feedparser.parse(self.url)

    def test_clear_text(self):
        self.assertEqual(clear_text("&#39;"), "'")

    def test_get_info_about_image(self):
        self.assertEqual(get_info_about_image(self.summary), '''NATO ally expels undercover Russian spy ''')

    def test_get_briefly_about_news(self):
        self.assertEqual(get_briefly_about_news(self.summary),
                         '''In a rare move,NATO ally Bulgaria has expelled an undercover '''
                         '''spy affiliated with the Russian military intelligence'''
                         ''' service, according to a Western intelligence source.''')

    def test_valid_date(self):
        self.assertEqual(str(valid_date("20191211")), "2019-12-11 00:00:00")
        with self.assertRaises(ValueError) as error:
            valid_date("dfgh")
        self.assertEqual(str(error.exception), 'Incorrect data format, should be YYYYMMDD')
        with self.assertRaises(ValueError) as error:
            valid_date("20102111")
        self.assertEqual(str(error.exception), 'Incorrect data format, should be YYYYMMDD')

    def test_get_news_feed(self):
        with self.assertRaises(URLError) as error:
            get_news_feed("wcxqa")
        self.assertEqual(str(error.exception), '<urlopen error syntax error>')
        with self.assertRaises(URLError) as error:
            get_news_feed(" https://news.tut.by/")
        self.assertEqual(str(error.exception), '<urlopen error not well-formed (invalid token)>')
        self.assertEqual(get_news_feed(self.url), self.news_feed)

    def test_init_list_of_news(self):

        list_of_news = []
        init_list_of_news(list_of_news, self.news_feed, 2)
        self.assertEqual(len(list_of_news), 2)


if __name__ == '__main__':
    unittest.main()
