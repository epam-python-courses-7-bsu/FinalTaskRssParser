import sys
from contextlib import closing
from dateutil import parser

sys.path.insert(1, 'final_task/rss_reader')
import database
import unittest
import exceptions


class TestNews(unittest.TestCase):
    def test_is_table(self):
        self.assertEqual(database.is_table("NEWSFA"), False)

    def test_read_news(self):
        with closing(database.connect_to_database())as con:
            cursor = con.cursor()
            database.create_table(con, cursor)
            date = parser.parse("10011001")
            list_of_news = []
            with self.assertRaises(exceptions.DataBaseEmpty) as error:
                database.read_news(list_of_news, 2, "not link", date, cursor)
            self.assertEqual(str(error.exception), 'Your news story on is empty ')

