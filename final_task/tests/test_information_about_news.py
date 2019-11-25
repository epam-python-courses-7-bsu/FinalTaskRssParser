import sys

sys.path.insert(1, 'final_task/rss_reader')
from information_about_news import *
import unittest
from io import StringIO
from unittest.mock import patch

class TestInformationAboutNews(unittest.TestCase):

    def setUp(self):
        self.description_from_website = '<p><a href="https://news.yahoo.com/protests-snake-kills-indian-schoolgirl' \
                                        '-class-135559540.html"><img src="http://l2.yimg.com/uu/api/res/1.2/iKaHCL' \
                                        'lg9vdX0PDZ4ZGHYA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenf' \
                                        's.com/en_us/News/afp.com/41e95a0b70637cceca42280de069ef90ce41026d.jpg" wi' \
                                        'dth="130" height="86" alt="Protests after snake kills Indian schoolgirl i' \
                                        'n class" align="left" title="Protests after snake kills Indian schoolgirl' \
                                        ' in class" border="0" ></a>Students at an Indian school protested Friday ' \
                                        'after a 10-year-old pupil died after being bitten by a snake lurking in a' \
                                        ' hole under her desk.<p><br clear="all">'

        self.news = InfoAboutNews(["https://news.yahoo.com/rss/",

                                   "Protests after snake kills Indian schoolgirl in class",

                                   "Fri, 22 Nov 2019 08:55:59 -0500",

                                   "[image: Protests after snake kills Indian schoolgirl in class][2]Students at an "
                                   "Indian school protested Friday after a 10-year-old pupil died after being bitten "
                                   "by a snake lurking in a hole under her desk.",

                                   "https://news.yahoo.com/protests-snake-kills-indian-schoolgirl-class-135559540.html",

                                   "http://l2.yimg.com/uu/api/res/1.2/iKaHCLlg9vdX0PDZ4ZGHYA--/YXBwaWQ9eXRhY2h5b247aD04"
                                   "Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/41e95a0b70637cceca42280de069"
                                   "ef90ce41026d.jpg"])

        self.output = "Title: Protests after snake kills Indian schoolgirl in class\n"
        self.output += "Date: Fri, 22 Nov 2019 08:55:59 -0500\n"
        self.output += "Link: https://news.yahoo.com/protests-snake-kills-indian-schoolgirl-class-135559540.html\n"
        self.output += "\n[image: Protests after snake kills Indian schoolgirl in class][2]"
        self.output += "Students at an Indian school protested Friday after a 10-year-old pupil died after being " \
                       "bitten by a snake lurking in a hole under her desk.\n"
        self.output += "\nLinks:\n"
        self.output += "[1]: https://news.yahoo.com/protests-snake-kills-indian-schoolgirl-class-135559540.html\n"
        self.output += "[2]: http://l2.yimg.com/uu/api/res/1.2/iKaHCLlg9vdX0PDZ4ZGHYA--/YXBwaWQ9eXRhY2h5b247aD04" \
                       "Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/41e95a0b70637cceca42280de069" \
                       "ef90ce41026d.jpg\n"
        self.output += '__________________________________________________________________'

    def test_find_description(self):
        self.assertEqual(find_description(self.description_from_website), "Students at an Indian school protested "
                                                                          "Friday after a 10-year-old pupil died "
                                                                          "after being bitten by a snake lurking "
                                                                          "in a hole under her desk.")

    def test_print_news(self):
        with patch('sys.stdout', new=StringIO()) as fake_out_put:
            printing(self.news)
            self.assertEqual(fake_out_put.getvalue().strip(), self.output)

if __name__ == '__main__':
    unittest.main()