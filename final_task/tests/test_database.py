import sys
from contextlib import closing
from dateutil import parser
import os

sys.path.insert(1, 'final_task/rss_reader')
import database
import unittest
import exceptions
from News import News


class TestNews(unittest.TestCase):
    @staticmethod
    def delete_database(database_name):
        if os.path.isfile(database_name):
            os.remove(database_name)

    def setUp(self):
        self.item = News(feed="feed",
                         title="title",
                         date=parser.parse("2019-11-17 10:44:20-05:00"),
                         link="link",
                         info_about_image="info_about_image",
                         briefly_about_news="briefly_about_news",
                         links_from_news=["link", "link_on_image"]
                         )

    def test_is_table(self):
        with closing(database.connect_to_database('database_fail.db'))as con:
            self.assertEqual(database.is_table(con, "NEWSFA", 'database_test.db'), False)
        if os.path.isfile('database_test.db'):
            os.remove('database_test.db')

    def test_read_news(self):
        with closing(database.connect_to_database('database_fail.db'))as con:
            cursor = con.cursor()
            database.create_table(con, cursor, 'database_fail.db')
            date = parser.parse("10011001")
            list_of_news = []
            with self.assertRaises(exceptions.DataBaseEmpty) as error:
                database.read_news(list_of_news, 2, "not link", date, cursor)
            self.assertEqual(str(error.exception), 'Your news story on is empty ')
        self.delete_database('database_fail.db')

    def test_create_table(self):
        with closing(database.connect_to_database('databasefail.db'))as con:
            database.create_table(con, con.cursor(), 'databasefail.db')
            self.assertTrue(database.is_table(con, "NEWS", 'databasefail.db'))
        self.delete_database('databasefail.db')

    def test_write_to(self):
        with closing(database.connect_to_database('databasefail_wr.db'))as con:
            database.create_table(con, con.cursor(), 'databasefail_wr.db')
            database.write_to([self.item, ], self.item.link, con.cursor())
            list_of_news = []
            database.read_news(list_of_news, 1, self.item.link, self.item.date, con.cursor())
            self.assertEqual(len(list_of_news), 1)
        self.delete_database('databasefail_wr.db')


if __name__ == '__main__':
    unittest.main()
