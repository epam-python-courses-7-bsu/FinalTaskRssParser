import unittest
from dominate import document

import rss_get_items
import converting
import printers


class RSSReaderTests(unittest.TestCase):

    def test_link_determine(self):
        link_examples = [
            "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
            "https://news.yahoo.com/rss/",
            "https://news.tut.by/rss/all.rss",
        ]
        for link in link_examples:
            self.assertEqual(type(rss_get_items.get_items(link)), list)

    def test_delete_html_in_description(self):
        self.assertEqual(rss_get_items.description('Times Company<p><br clear="all">'),
                         'Times Company')
        self.assertEqual(rss_get_items.description('<p>America grapples with<p>'),
                         'America grapples with')
        self.assertEqual(rss_get_items.description('<p><a>https://news.yahoo.com/duterte-fires-vice-president-post'
                                                   '-125402618.html'),
                         'https://news.yahoo.com/duterte-fires-vice-president-post-125402618.html')

    def test_converting_to_html(self):
        item = [{'title': '«Ленинград» снова собрал забитую «Минск-Арену». И вот как это было',
                 'content': ['https://img.tyt.by/n/sport/07/f/maradona_brest_2018_1_6.jpg'],
                 'pubDate': 'Sun, 24 Nov 2019 21:53:00 +0300',
                 'description': '<img src="https://img.tyt.by/thumbnails/n/afisha/06/2'
                                '/leningrad_yerch_tutby_phsl_20191124_yyd_3862.jpg" width="72" height="48"'
                                ' alt="Фото: Евгений Ерчак, TUT.BY" border="0" align="left" hspace="5"'
                                ' />В воскресенье в Минске отгремел концерт группы «Ленинград».'
                                ' Отгремел, как всегда, с аншлагом - «Минск-Арена» была забита до отказу. '
                                'Как фанаты отрывались в этот вечер под известные хиты - в фоторепортаже TUT.BY.<br '
                                'clear="all" />',
                 'link': 'https://sport.tut.by/news/football/662512.html?'
                         'utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news'},
                {'title': '«Ленинград» снова собрал забитую «Минск-Арену». И вот как это было',
                 'content': ['https://img.tyt.by/n/sport/07/f/maradona_brest_2018_1_6.jpg'],
                 'pubDate': 'Sun, 24 Nov 2019 21:53:00 +0300',
                 'description': '<img src="https://img.tyt.by/thumbnails/n/afisha/06/2'
                                '/leningrad_yerch_tutby_phsl_20191124_yyd_3862.jpg" width="72" height="48"'
                                ' alt="Фото: Евгений Ерчак, TUT.BY" border="0" align="left" hspace="5"'
                                ' />В воскресенье в Минске отгремел концерт группы «Ленинград».'
                                ' Отгремел, как всегда, с аншлагом - «Минск-Арена» была забита до отказу. '
                                'Как фанаты отрывались в этот вечер под известные хиты - в фоторепортаже TUT.BY.<br '
                                'clear="all" />',
                 'link': 'https://sport.tut.by/news/football/662512.html?'
                         'utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news'}]
        self.assertEqual(type(converting.create_html(item)), document)

    def test_make_json_format(self):
        item = [{'title': '«Ленинград» снова собрал забитую «Минск-Арену». И вот как это было',
                 'content': ['https://img.tyt.by/n/sport/07/f/maradona_brest_2018_1_6.jpg'],
                 'pubDate': 'Sun, 24 Nov 2019 21:53:00 +0300',
                 'description': '<img src="https://img.tyt.by/thumbnails/n/afisha/06/2'
                                '/leningrad_yerch_tutby_phsl_20191124_yyd_3862.jpg" width="72" height="48"'
                                ' alt="Фото: Евгений Ерчак, TUT.BY" border="0" align="left" hspace="5"'
                                ' />В воскресенье в Минске отгремел концерт группы «Ленинград».'
                                ' Отгремел, как всегда, с аншлагом - «Минск-Арена» была забита до отказу. '
                                'Как фанаты отрывались в этот вечер под известные хиты - в фоторепортаже TUT.BY.<br '
                                'clear="all" />',
                 'link': 'https://sport.tut.by/news/football/662512.html?'
                         'utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news'},
                {'title': '«Ленинград» снова собрал забитую «Минск-Арену». И вот как это было',
                 'content': ['https://img.tyt.by/n/sport/07/f/maradona_brest_2018_1_6.jpg'],
                 'pubDate': 'Sun, 24 Nov 2019 21:53:00 +0300',
                 'description': '<img src="https://img.tyt.by/thumbnails/n/afisha/06/2'
                                '/leningrad_yerch_tutby_phsl_20191124_yyd_3862.jpg" width="72" height="48"'
                                ' alt="Фото: Евгений Ерчак, TUT.BY" border="0" align="left" hspace="5"'
                                ' />В воскресенье в Минске отгремел концерт группы «Ленинград».'
                                ' Отгремел, как всегда, с аншлагом - «Минск-Арена» была забита до отказу. '
                                'Как фанаты отрывались в этот вечер под известные хиты - в фоторепортаже TUT.BY.<br '
                                'clear="all" />',
                 'link': 'https://sport.tut.by/news/football/662512.html?'
                         'utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news'}]
        self.assertEqual(type(printers.make_json(item)), dict)

    def test_data_split(self):
        self.assertEqual(printers.data_split("Sun, 24 Nov 2019 11:48: 25 -0500"), "24/11/2019")
        self.assertEqual(printers.data_split("Sat, 25 Dec 2019 12:12: 15 - 0540"), "25/12/2019")
        self.assertEqual(printers.data_split("Mon, 23 Jun 2000 14:34: 12 - 0988"), "23/06/2000")

    def test_filter_title(self):
        self.assertEqual(printers.filter_title("Indian fox killing pe&#39;ople in Belarus"),
                         "Indian fox killing people in Belarus")
        self.assertEqual(printers.filter_title("Somet&#39;imes he goes&#39; for a&#39; walk"),
                         "Sometimes he goes for a walk")
        self.assertEqual(printers.filter_title("This is &#39;some tests for &#39;this to&#39;ol"),
                         "This is some tests for this tool")

    def test_split_by_lines(self):
        self.assertEqual(printers.split_string_by_lines("Indian fox killing people in Belarus", 1),
                         "Indian\nfox\nkilling\npeople\nin\nBelarus")

        self.assertEqual(printers.split_string_by_lines("Sometimes he goes for a walk", 2),
                         "Sometimes he\ngoes for\na walk")


if __name__ == "__main__":
    unittest.main()
