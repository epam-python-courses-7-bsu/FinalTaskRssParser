import sys
sys.path.insert(1, 'final_task/rss_reader')
from database_functions import *
import unittest
from io import StringIO
from unittest.mock import patch

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):

        self.news = ["https://news.yahoo.com/rss/", "Protests after snake kills Indian schoolgirl in class",
                     "Fri, 22 Nov 2019 08:55:59 -0500", "[image: Protests after snake kills Indian schoolgirl in class]"
                     "[2]Students at an Indian school protested Friday after a 10-year-old pupil died after being "
                     "bitten by a snake lurking in a hole under her desk.", "https://news.yahoo.com/protests-snake-"
                     "kills-indian-schoolgirl-class-135559540.html", "http://l2.yimg.com/uu/api/res/1.2/iKaHCLlg9vdX0PD"
                     "Z4ZGHYA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/41e95a0b"
                     "70637cceca42280de069ef90ce41026d.jpg"]

    def test_exist_table(self):
        self.assertEqual(check_existance("new"), False)

    def test_print_in_json_format(self):
        self.result = "[\n     {\n"
        self.result += '          "Title": "Protests after snake kills Indian schoolgirl in class",\n'
        self.result += '          "Date": "Fri, 22 Nov 2019 08:55:59 -0500",\n'
        self.result += '          "Description": "[image: Protests after snake kills Indian schoolgirl in class][2]' \
                       'Students at an Indian school protested Friday after a 10-year-old pupil died after being bi' \
                       'tten by a snake lurking in a hole under her desk.",\n'
        self.result += '          "Link [1]": "https://news.yahoo.com/protests-snake-kills-indian-schoolgirl-class-' \
                       '135559540.html",\n'
        self.result += '          "Link [2]": "http://l2.yimg.com/uu/api/res/1.2/iKaHCLlg9vdX0PDZ4ZGHYA--/YXBwaWQ9e' \
                       'XRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/41e95a0b70637cceca422' \
                       '80de069ef90ce41026d.jpg"\n'
        self.result += "     }\n]"
        with patch('sys.stdout', new=StringIO()) as fake_out_put:
            json_from_cashe([self.news])
            self.assertEqual(fake_out_put.getvalue().strip(), self.result)

if __name__ == '__main__':
    unittest.main()