import sys
sys.path.insert(1, 'final_task/rss_reader')
from conversion_functions import *
import unittest
from unittest.mock import patch

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):

        self.dict_of_args = {
            "url": "https://news.yahoo.com/rss/",
            "lim": 1,
            "json": False,
            "date": "20191125",
            "path": r"C:\Users\Lenovo\PycharmProjects\final_task\FinalTaskRssParser\final_task\tests",
            "html": True,
            "pdf": False}

        self.news = ["https://news.yahoo.com/rss/", "Protests after snake kills Indian schoolgirl in class",
                     "Fri, 22 Nov 2019 08:55:59 -0500", "[image: Protests after snake kills Indian schoolgirl in class]"
                     "[2]Students at an Indian school protested Friday after a 10-year-old pupil died after being "
                     "bitten by a snake lurking in a hole under her desk.", "https://news.yahoo.com/protests-snake-"
                     "kills-indian-schoolgirl-class-135559540.html", "http://l2.yimg.com/uu/api/res/1.2/iKaHCLlg9vdX0PD"
                     "Z4ZGHYA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/41e95a0b"
                     "70637cceca42280de069ef90ce41026d.jpg"]

        self.path = r"C:\Users\Lenovo\PycharmProjects\final_task\FinalTaskRssParser\final_task\tests"

        self.result_of_conversion = '<h1>News from https://news.yahoo.com/rss/</h1>' \
                                    '<item><h2>Protests after snake kills Indian schoolgirl in class</h2>' \
                                    '<link>https://news.yahoo.com/protests-snake-kills-indian-schoolgirl-class-135' \
                                    '559540.html</link>' \
                                    '<p>Fri, 22 Nov 2019 08:55:59 -0500</p>' \
                                    '<h3><img src="http://l2.yimg.com/uu/api/res/1.2/iKaHCLlg9vdX0PDZ4ZGHYA--/YXBw' \
                                    'aWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/41' \
                                    'e95a0b70637cceca42280de069ef90ce41026d.jpg" ' \
                                    'alt="http://l2.yimg.com/uu/api/res/1.2/iKaHCLlg9vdX0PDZ4ZGHYA--/YXBwaWQ9eXRhY' \
                                    '2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/41e95a0b706' \
                                    '37cceca42280de069ef90ce41026d.jpg" border="0" align="left" hspace="5"></img>' \
                                    '[image: Protests after snake kills Indian schoolgirl in class][2]Students at' \
                                    ' an Indian school protested Friday after a 10-year-old pupil died after being ' \
                                    'bitten by a snake lurking in a hole under her desk.</h3><br><br></br></br></item>'

    def test_get_path_to_file(self):
        self.assertEqual(get_path(self.path, "pdf"),
                         r"C:\Users\Lenovo\PycharmProjects\final_task\FinalTaskRssParser\final_task\tests\news.pdf")
        self.assertEqual(get_path("dch", "pdf"), None)

    def test_convert(self):
        document = convert_into_html_format([self.news], self.dict_of_args)
        self.assertEqual(document, self.result_of_conversion)

if __name__ == '__main__':
    unittest.main()