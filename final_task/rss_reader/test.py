import os
import unittest
from Handler import parse_to_json
from Handler import Handler
from News import News

from WorkWithCache import save_img
from WorkWithCache import read_from_file


class TestEntry(unittest.TestCase):
    def test__init__(self):
        news = News("news", "lll", "ttt", "55af5", ["jfajaf", "fakf"], "1223665")
        self.assertIsInstance(news, News)
        self.assertNotIsInstance("news", News)
        self.assertIsInstance(news.title, str)
        self.assertIsInstance(news.strDate, str)
        self.assertIsInstance(news.date, str)
        self.assertIsInstance(news.news, str)
        self.assertIsInstance(news.link, str)
        self.assertIsInstance(news.links, list)

    def test_parse_to_json(self):
        self.assertIsInstance(parse_to_json(News("news", "lll", "ttt", "55af5", ["jfajaf", "fakf"], "1223665")), dict)

    def test_get_all(self):
        url = "https://news.yahoo.com/rss/"
        lim = 3
        hand = Handler(url, lim)

        self.assertIsInstance(hand.get_all(), list)
        self.assertIsInstance(hand.get_all()[0], News)
        self.assertEqual(len(hand.get_all()), lim)

    def test_link(self):
        link = "https://news.yahoo.com/rss/"
        hand = Handler("https://news.yahoo.com/rss/", 3)
        self.assertEqual(hand.get_link(link), "https://news.yahoo.com")

    def test_img_link(self):
        text = 'img src="http://l.yimg.com/uu/api/res/1.2/I4AtbbFWPM.66LesQWxLqQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzM' \
               'Ds-/https://media.zenfs.com/en/the_new_york_times_articles_158/101bec76cc1717d8bfd63460b9443fd1" width=' \
               '"130" height="86" alt="She Texted About Dinner While Driving. Then a Pedestrian Was Dead." align="left" ' \
               'title="She Texted About Dinner While Driving. Then a Pedestrian Was Dead." border="0" ></a>FREEHOLD, N.J.' \
               ' -- One woman was out for a walk and a taste of fresh air during a break from her job as a scientist at' \
               ' a New Jersey fragrance manufacturer. She and her husband had been trying to get pregnant, and brief' \
               ' bouts of exercise, away from the laboratory&#39;s smells and fumes, were part of that plan.A second ' \
               'woman was behind the wheel of a black Mercedes-Benz, headed to work as chief executive of a nonprofit in '
        img_link = 'http://l.yimg.com/uu/api/res/1.2/I4AtbbFWPM.66LesQWxLqQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzM' \
                   'Ds-/https://media.zenfs.com/en/the_new_york_times_articles_158/101bec76cc1717d8bfd63460b9443fd1'
        hand = Handler("https://news.yahoo.com/rss/", 3)

        self.assertEqual(hand.get_img_links(text)[0], img_link)

    def test_img_link_2(self):
        text = 'img src="http://l.yimg.com/uu/api/res/1.2/I4AtbbFWPM.66LesQWxLqQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzM' \
               'Ds-/https://media.zenfs.com/en/the_new_york_times_articles_158/101bec76cc1717d8bfd63460b9443fd1" width=' \
               '"130" height="86" alt="She Texted About Dinner While Driving. Then a Pedestrian Was Dead." align="left" ' \
               'title="She Texted About Dinner While Driving. Then a Pedestrian Was Dead." border="0" ></a>FREEHOLD, N.J.' \
               ' -- One woman was out for a walk and a taste of fresh air during a break from her job as a scientist at' \
               ' a New Jersey fragrance manufacturer. She and her husband had been trying to get pregnant, and brief' \
               ' bouts of exercise, away from the laboratory&#39;s smells and fumes, were part of that plan.A second ' \
               'woman was behind the wheel of a black Mercedes-Benz, headed to work as chief executive of a nonprofit in '
        img_link = 'l.yimg.com/uu/api/res/1.2/I4AtbbFWPM.66LesQWxLqQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzM' \
                   'Ds-/https://media.zenfs.com/en/the_new_york_times_articles_158/101bec76cc1717d8bfd63460b9443fd1'
        hand = Handler("https://news.yahoo.com/rss/", 3)

        self.assertNotEqual(hand.get_img_links(text)[0], img_link)

    def test_img_alt(self):
        text = 'img src="http://l.yimg.com/uu/api/res/1.2/I4AtbbFWPM.66LesQWxLqQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzM' \
               'Ds-/https://media.zenfs.com/en/the_new_york_times_articles_158/101bec76cc1717d8bfd63460b9443fd1" width=' \
               '"130" height="86" alt="She Texted About Dinner While Driving. Then a Pedestrian Was Dead." align="left" ' \
               'title="She Texted About Dinner While Driving. Then a Pedestrian Was Dead." border="0" ></a>FREEHOLD, N.J.' \
               ' -- One woman was out for a walk and a taste of fresh air during a break from her job as a scientist at' \
               ' a New Jersey fragrance manufacturer. She and her husband had been trying to get pregnant, and brief' \
               ' bouts of exercise, away from the laboratory&#39;s smells and fumes, were part of that plan.A second ' \
               'woman was behind the wheel of a black Mercedes-Benz, headed to work as chief executive of a nonprofit in '
        img_alt = 'She Texted About Dinner While Driving. Then a Pedestrian Was Dead.'
        hand = Handler("https://news.yahoo.com/rss/", 3)

        self.assertEqual(hand.get_img_alt(text)[0], img_alt)

    def test_img_alt_2(self):
        text = 'img src="http://l.yimg.com/uu/api/res/1.2/I4AtbbFWPM.66LesQWxLqQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzM' \
               'Ds-/https://media.zenfs.com/en/the_new_york_times_articles_158/101bec76cc1717d8bfd63460b9443fd1" width=' \
               '"130" height="86" alt="She Texted About Dinner While Driving. Then a Pedestrian Was Dead." align="left" ' \
               'title="She Texted About Dinner While Driving. Then a Pedestrian Was Dead." border="0" ></a>FREEHOLD, N.J.' \
               ' -- One woman was out for a walk and a taste of fresh air during a break from her job as a scientist at' \
               ' a New Jersey fragrance manufacturer. She and her husband had been trying to get pregnant, and brief' \
               ' bouts of exercise, away from the laboratory&#39;s smells and fumes, were part of that plan.A second ' \
               'woman was behind the wheel of a black Mercedes-Benz, headed to work as chief executive of a nonprofit in '
        img_alt = '="She Texted About Dinner While Driving. Then a Pedestrian Was Dead.'
        hand = Handler("https://news.yahoo.com/rss/", 3)

        self.assertNotEqual(hand.get_img_alt(text)[0], img_alt)

    def test_html_parse(self):
        text = '<p><a href="https://news.yahoo.com/graham-trump-ukraine-incoherent-quid-pro-quo-192210175.html">' \
               '<img src="http://l2.yimg.com/uu/api/res/1.2/aWhGys7_IW5qIjKaiJpPfg--/YXBwaWQ9eXRhY2h5b247aD04Njt' \
               '3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/5527ffe0-00' \
               'ca-11ea-9f7d-d1e736c1315d" width="130" height="86" alt="Graham now says Trump&#39;s Ukraine poli' \
               'cy was too &#39;incoherent&#39; for quid pro quo" align="left" title="Graham now says Trump&#39;' \
               's Ukraine policy was too &#39;incoherent&#39; for quid pro quo" border="0" ></a>A day after sayi' \
               'ng he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and hi' \
               's conclusion is that the Trump administration’s Ukraine policy was too &quot;incoherent&quot; fo' \
               'r it to have orchestrated the quid pro quo at the heart of the impeachment inquiry.<p><br clear="all">'

        news = "[img 0 Graham now says Trump's Ukraine policy was too 'incoherent' for quid pro quo]A day after " \
               "saying he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and his " \
               "conclusion is that the Trump administration’s Ukraine policy was too \"incoherent\" for it to have" \
               " orchestrated the quid pro quo at the heart of the impeachment inquiry."

        hand = Handler("https://news.yahoo.com/rss/", 3)
        self.assertEqual(hand.parse_html(text), news)

    def test_html_parse_2(self):
        text = '<p><a href="https://news.yahoo.com/graham-trump-ukraine-incoherent-quid-pro-quo-192210175.html">' \
               '<img src="http://l2.yimg.com/uu/api/res/1.2/aWhGys7_IW5qIjKaiJpPfg--/YXBwaWQ9eXRhY2h5b247aD04Njt' \
               '3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/5527ffe0-00' \
               'ca-11ea-9f7d-d1e736c1315d" width="130" height="86" alt="Graham now says Trump&#39;s Ukraine poli' \
               'cy was too &#39;incoherent&#39; for quid pro quo" align="left" title="Graham now says Trump&#39;' \
               's Ukraine policy was too &#39;incoherent&#39; for quid pro quo" border="0" ></a>A day after sayi' \
               'ng he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and hi' \
               's conclusion is that the Trump administration’s Ukraine policy was too &quot;incoherent&quot; fo' \
               'r it to have orchestrated the quid pro quo at the heart of the impeachment inquiry.<p><br clear="all">'

        news = "A day after " \
               "saying he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and his " \
               "conclusion is that the Trump administration’s Ukraine policy was too \"incoherent\" for it to have" \
               " orchestrated the quid pro quo at the heart of the impeachment inquiry."

        hand = Handler("https://news.yahoo.com/rss/", 3)
        self.assertNotEqual(hand.parse_html(text), news)

    def test_save_img(self):
        url = "http://l1.yimg.com/uu/api/res/1.2/e2khNA0h_dG4YdzIfYpnMA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://" \
              "media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/fa203490-0d54-11ea-b6b2-f04309019748"
        name = "nameimgnameimgnameimgnameimg"
        save_img(url, name)
        self.assertTrue(os.path.exists(f'images/{name}.jpg'))

    def test_read_file(self):
        news=read_from_file(20191121,1)
        self.assertEqual(news[0]["title"],"House Democrats ponder expanding impeachment probe after Sondland 'game change"
                                       "r' testimony")
    def test_read_filee(self):
        news = read_from_file(20191121, 1)
        self.assertEqual(news[0]["link"],"https://news.yahoo.com")
    def test_read_file_lenght(self):
        lim=3
        news = read_from_file(20191121, 3)
        self.assertEqual(len(news), lim)
if __name__ == '__main__':
    unittest.main()