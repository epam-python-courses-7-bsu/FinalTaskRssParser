import unittest
import sys
import requests.exceptions as rexc
import os
sys.path.append('../rss_reader')
import rss_reader
import CSVEntities
import ClassNews
import ToPDF
import ToHTML
import logging


TEST_LIST = [
    ClassNews.Article(
        'On an upswing, the Pete Buttigieg show rolls through New Hampshire',
        'Sat, 17 Nov 2019 09:36:14 -0500',
            'https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.html',
            'Pete Buttigieg traveled more than 100 miles through the Granite State on a busemblazoned'
            ' with his name and packed with over a dozen journalists. It\'s aspectacle that hasn\'t been '
            'seen in recent presidential races, but it\'s part ofa freewheeling strategy has helped bring '
            'Buttigieg from relative obscurity tothe top of the Democratic primary field. ',
            '<p><a href="https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.'
            'html"><img src="http://l2.yimg.com/uu/api/res/1.2/cqp8V_ndESsAGfj_ke5adw--/YXBwaWQ9eXR'
            'hY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-'
            'images/2019-11/9e842ef0-04eb-11ea-a66f-fec562b3bef1" width="130" height="86" alt="On '
            'an upswing, the Pete Buttigieg show rolls through New Hampshire" align="left" title='
            '"On an upswing, the Pete Buttigieg show rolls through New Hampshire" border="0" ></a>'
            'Pete Buttigieg traveled more than 100 miles through the Granite State on a bus '
            'emblazoned with his name and packed with over a dozen journalists. It’s a spectacle '
            'that hasn’t been seen in recent presidential races, but it’s part of a freewheeling '
            'strategy has helped bring Buttigieg from relative obscurity to the top of the '
            'Democratic primary field. <p><br clear="all">'.replace('\n',"")
    ),
    ClassNews.Article(
        'NATO ally expels undercover Russian spy ',
        'Sat, 16 Nov 2019 16:11:50 -0500',
        'https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html',
        'In a rare move, NATO ally Bulgaria has expelled an undercover spy affiliated '
        'with the Russian military intelligence service, according to a Westernintelligence source.',
         '<p><a href="https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-'
         '211150048.html"><img src="http://l1.yimg.com/uu/api/res/1.2/IKBjTl0jeU0BCnrjqbCKAw--'
         '/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com'
         '/creatr-uploaded-images/2019-11/440e0010-0714-11ea-9bcb-45ff7f6277b3" width="130" '
        'height="86" alt="NATO ally expels undercover Russian spy " align="left" title='
        '"NATO ally expels undercover Russian spy " border="0" ></a>In a rare move, NATO '
        'ally Bulgaria has expelled an undercover spy affiliated with the Russian military '
        'intelligence service, according to a Western intelligence source.<p><br clear='
         '"all">'.replace('\n', '')
   )
]
TEST_LIST_DICT = [
    {
        'title': 'On an upswing, the Pete Buttigieg show rolls through New Hampshire',
        'date': 'Sat, 17 Nov 2019 09:36:14 -0500',
        'link': 'https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.html',
        'article': "Pete Buttigieg traveled more than 100 miles through the Granite State on a busembla"
                   "zoned with his name and packed with over a dozen journalists. It's aspectacle that ha"
                   "sn't been seen in recent presidential races, but it's part ofa freewheeling strategy "
                   "has helped bring Buttigieg from relative obscurity tothe top of the Democratic primary"
                   " field. ",
        'links': ['https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.html',
                  'http://l2.yimg.com/uu/api/res/1.2/cqp8V_ndESsAGfj_ke5adw--/YXBwaWQ9eXRhY2h5b247aD04Nj'
                  't3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/9e'
                  '842ef0-04eb-11ea-a66f-fec562b3bef1'
                  ]
    },
    {
        'title': 'NATO ally expels undercover Russian spy ',
        'date': 'Sat, 16 Nov 2019 16:11:50 -0500',
        'link': 'https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html',
        'article': 'In a rare move, NATO ally Bulgaria has expelled an undercover spy affiliated with the'
                   ' Russian military intelligence service, according to a Westernintelligence source.',
        'links': ['https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html',
                  'http://l1.yimg.com/uu/api/res/1.2/IKBjTl0jeU0BCnrjqbCKAw--/YXBwaWQ9eXRhY2h5b247aD04Nj'
                  't3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/'
                  '440e0010-0714-11ea-9bcb-45ff7f6277b3'
        ]
    }
]


class RssReaderTestCase(unittest.TestCase):
    def test_html_to_links(self):
        self.assertTrue(ClassNews.html_text_to_list_links(
            "<p><a href=\"https://news.yahoo.com/syracuse-suspends-fraternity-activities-string-150512659.html\"><img "
            "src=\"http://l.yimg.com/uu/api/res/1.2/WtsFIK_rUo0Z_cSM4WlEhA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https"
            "://media.zenfs.com/en-us/usa_today_news_641/0303a78836e137c91b44145a8c735262\" width=\"130\" height=\"86\""
            " alt=\"Racist, anti-Semitic incidents prompt Syracuse to halt fraternity activities; Alpha Chi Rho "
            "suspended\" align=\"left\" title=\"Racist, anti-Semitic incidents prompt Syracuse to halt fraternity "
            "activities; Alpha Chi Rho suspended\" border=\"0\" ></a>Syracuse suspended a fraternity and halted social "
            "activities at all of them for the semester after a series of racist and anti-Semitic incidents.<p><br "
            "clear=\"all\">"
        )),[
            'https://news.yahoo.com/syracuse-suspends-fraternity-activities-string-150512659.html',
           'http://l.yimg.com/uu/api/res/1.2/WtsFIK_rUo0Z_cSM4WlEhA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://medi'
           'a.zenfs.com/en-us/usa_today_news_641/0303a78836e137c91b44145a8c735262'
        ]

    def test_dicts_to_articles(self):
        self.assertEqual(
            ClassNews.dicts_to_articles([{
                        'date': 'Sat, 17 Nov 2019 09:36:14 -0500',
                        'title': 'On an upswing, the Pete Buttigieg show rolls through New Hampshire',
                        'link': 'https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.html',
                        'article': 'Pete Buttigieg traveled more than 100 miles through the Granite State on a '
                                   'busemblazoned with his name and packed with over a dozen journalists. It\'s '
                                   'aspectacle that hasn\'t been seen in recent presidential races, but it\'s part ofa '
                                   'freewheeling strategy has helped bring Buttigieg from relative obscurity tothe top '
                                   'of the Democratic primary field. ',
                        'links': '<p><a href="https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.'
                                 'html"><img src="http://l2.yimg.com/uu/api/res/1.2/cqp8V_ndESsAGfj_ke5adw--/YXBwaW'
                                 'Q9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-'
                                 'uploaded-images/2019-11/9e842ef0-04eb-11ea-a66f-fec562b3bef1" width="130" height="86"'
                                 ' alt="On an upswing, the Pete Buttigieg show rolls through New Hampshire" align="left'
                                 '" title="On an upswing, the Pete Buttigieg show rolls through New Hampshire" '
                                 'border="0" ></a> Pete Buttigieg traveled more than 100 miles through the Granite '
                                 'State on a bus emblazoned with his name and packed with over a dozen journalists.'
                                 ' It’s a spectacle that hasn’t been seen in recent presidential races, but it’s part '
                                 'of a freewheeling strategy has helped bring Buttigieg from relative obscurity to the'
                                 ' top of the Democratic primary field. <p><br clear="all">'.replace('\n', "")
                    },
                        {
                            'title': 'NATO ally expels undercover Russian spy ',
                            'date': 'Sat, 16 Nov 2019 16:11:50 -0500',
                            'link': 'https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html',
                            'article': 'In a rare move, NATO ally Bulgaria has expelled an undercover spy affiliated '
                                           'with the Russian military intelligence service, according to a '
                                       'Westernintelligence source.',
                            'links': '<p><a href="https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-'
                                     '211150048.html"><img src="http://l1.yimg.com/uu/api/res/1.2/IKBjTl0jeU0BCnrjqbC'
                                     'KAw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.'
                                     'amazonaws.com/creatr-uploaded-images/2019-11/440e0010-0714-11ea-9bcb-45ff7f6277b3'
                                     '" width="130" height="86" alt="NATO ally expels undercover Russian spy " align='
                                     '"left" title="NATO ally expels undercover Russian spy " border="0" ></a>In a rare'
                                     ' move, NATO ally Bulgaria has expelled an undercover spy affiliated with the '
                                     'Russian military intelligence service, according to a Western intelligence '
                                     'source.<p><br clear="all">'.replace('\n', '')
                        }
                ]
            ), TEST_LIST
        )

    def test_write_csv(self):
        self.assertEqual(CSVEntities.csv_to_python(TEST_LIST, 'rss_test.csv'), True)

    def test_args_parser(self):
        parser = rss_reader.args_parser(['https://news_api.com', '--version', '--json', '--verbose', '--limit', '2',
                                         '--date', '20191119','--to-pdf', 'd:/set', '--to-html', 'd:/set'])
        self.assertEqual(parser.source, 'https://news_api.com')
        self.assertTrue(parser.version)
        self.assertTrue(parser.json)
        self.assertTrue(parser.verbose)
        self.assertEqual(parser.limit, 2)
        self.assertEqual(parser.date, '20191119')
        self.assertEqual(parser.to_pdf, 'd:/set')
        self.assertEqual(parser.to_html, 'd:/set')
    def test_pdf_writing(self):
        path = os.path.dirname(__file__)
        self.assertEqual(ToPDF.print_article_list_to_pdf(TEST_LIST, path), True)
    def test_pdf_writing(self):
        path = os.path.dirname(__file__)
        self.assertEqual(rss_reader.convert_to_pdf(TEST_LIST, path), True)

    def test_requests(self):
        self.assertEqual(rss_reader.get_request('https://news.yahoo.com/rss').status_code, 200)

    def test_requests_exceptions_inv_schema(self):
        self.assertRaises(rexc.InvalidSchema, rss_reader.get_request, 'htps://news.yahoo.com')

    def test_requests_exceptions_read_timeout(self):
        self.assertRaises(rexc.Timeout, rss_reader.get_request, 'https://news.yahoo.com', timeout=(1, 0.01))

    def test_requests_exceptions_httperror(self):
        self.assertRaises(rexc.HTTPError, rss_reader.get_request, 'https://yahoo.com/rss')

    def test_to_pdf_exceptions(self):
        self.assertRaises(FileNotFoundError, rss_reader.convert_to_pdf, TEST_LIST, 'c:/somenonexistdir')

    def test_to_html_exceptions(self):
        self.assertRaises(FileNotFoundError, rss_reader.convert_to_html, TEST_LIST, 'c:/somenonexistdir')

    def test_articles_to_dict_articles(self):
        self.assertEqual(rss_reader.articles_to_dict_articles(TEST_LIST),
        [
            {
                'title': 'On an upswing, the Pete Buttigieg show rolls through New Hampshire',
                'date': 'Sat, 17 Nov 2019 09:36:14 -0500',
                'link': 'https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.html',
                'article': "Pete Buttigieg traveled more than 100 miles through the Granite State on a busembla"
                           "zoned with his name and packed with over a dozen journalists. It's aspectacle that ha"
                           "sn't been seen in recent presidential races, but it's part ofa freewheeling strategy "
                           "has helped bring Buttigieg from relative obscurity tothe top of the Democratic primary"
                           " field. ",
                'links': ['https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.html',
                          'http://l2.yimg.com/uu/api/res/1.2/cqp8V_ndESsAGfj_ke5adw--/YXBwaWQ9eXRhY2h5b247aD04Nj'
                          't3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/9e'
                          '842ef0-04eb-11ea-a66f-fec562b3bef1'
                          ]
            },
            {
                'title': 'NATO ally expels undercover Russian spy ',
                'date': 'Sat, 16 Nov 2019 16:11:50 -0500',
                'link': 'https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html',
                'article': 'In a rare move, NATO ally Bulgaria has expelled an undercover spy affiliated with the'
                           ' Russian military intelligence service, according to a Westernintelligence source.',
                'links': ['https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html',
                          'http://l1.yimg.com/uu/api/res/1.2/IKBjTl0jeU0BCnrjqbCKAw--/YXBwaWQ9eXRhY2h5b247aD04Nj'
                          't3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/'
                          '440e0010-0714-11ea-9bcb-45ff7f6277b3'
                ]
            }
        ]
    )

    def test_logger_critical(self):
        logging_level = logging.CRITICAL
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)
        self.assertEqual(rss_reader.rss_logging(logging, "message", 'critical'), logging.critical("message"))
        self.assertEqual(rss_reader.rss_logging(logging, "message", 'warning'),  logging.warning("message"))
        self.assertEqual(rss_reader.rss_logging(logging, "message", 'info'),  logging.info("message"))

    def test_logger_info(self):
        logging_level = logging.INFO
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)
        self.assertEqual(rss_reader.rss_logging(logging, "message", 'critical'), logging.critical("message"))
        self.assertEqual(rss_reader.rss_logging(logging, "message", 'warning'), logging.warning("message"))
        self.assertEqual(rss_reader.rss_logging(logging, "message", 'info'), logging.info("message"))

    def test_list_to_json(self):
        self.assertEqual(
            TEST_LIST_DICT,
            [
                {
                    "title": "On an upswing, the Pete Buttigieg show rolls through New Hampshire",
                    "date": "Sat, 17 Nov 2019 09:36:14 -0500",
                    "link": "https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.html",
                    "article": "Pete Buttigieg traveled more than 100 miles through the Granite State on a busemblaz"
                               "oned with his name and packed with over a dozen journalists. It's aspectacle that ha"
                               "sn't been seen in recent presidential races, but it's part ofa freewheeling strategy ha"
                               "s helped bring Buttigieg from relative obscurity tothe top of the Democratic primary "
                               "field. ",
                    "links": [
                        "https://news.yahoo.com/pete-buttigieg-bus-tour-upswing-polls-143614985.html",
                        "http://l2.yimg.com/uu/api/res/1.2/cqp8V_ndESsAGfj_ke5adw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTE"
                        "zMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/9e842ef0-04"
                        "eb-11ea-a66f-fec562b3bef1"
                    ]
                },
                {
                    "title": "NATO ally expels undercover Russian spy ",
                    "date": "Sat, 16 Nov 2019 16:11:50 -0500",
                    "link": "https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html",
                    "article": "In a rare move, NATO ally Bulgaria has expelled an undercover spy affiliated with the "
                               "Russian military intelligence service, according to a Westernintelligence source.",
                    "links": [
                        "https://news.yahoo.com/nato-ally-expels-undercover-russian-spy-211150048.html",
                        "http://l1.yimg.com/uu/api/res/1.2/IKBjTl0jeU0BCnrjqbCKAw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTE"
                        "zMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/440e0010-071"
                        "4-11ea-9bcb-45ff7f6277b3"
                    ]
                }
            ]

        )


if __name__ == '__main__':
    unittest.main()
