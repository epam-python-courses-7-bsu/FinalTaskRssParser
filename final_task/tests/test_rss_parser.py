import sys
sys.path.insert(1, 'final_task/rss_reader')
from rss_parser import *
from database_functions import *
import unittest
from io import StringIO
from unittest.mock import patch

class TestParseFunctions(unittest.TestCase):
    def setUp(self):

        self.dict_of_args = {
            "url": "https://news.yahoo.com/rss/",
            "lim": 1,
            "json": False,
            "date": "20191122",
            "path": r"C:\Users\Lenovo\PycharmProjects\final_task\FinalTaskRssParser\final_task\tests",
            "html": True,
            "pdf": False}

    def test_read_news(self):
        with patch('sys.stdout', new=StringIO()) as fake_out_put:
            print_cache(self.dict_of_args)
            self.assertEqual(fake_out_put.getvalue().strip(), 'No results\nTry to enter another date or url')

if __name__ == '__main__':
    unittest.main()