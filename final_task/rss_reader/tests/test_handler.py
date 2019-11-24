import os
import sys
import unittest

out_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(out_dir)
from Handler import Handler
from Entry import Entry
from RSSReaderException import RSSReaderException
from io import StringIO
from unittest.mock import patch, mock_open, MagicMock


class TestHandler(unittest.TestCase):
    def test__init__(self):
        handler = Handler("https://news.yahoo.com/rss/", 1, 1.0)
        self.assertIsInstance(handler, Handler)
        self.assertNotIsInstance("handler", Handler)

    def setUp(self):
        self.handler = Handler("https://news.yahoo.com/rss/", 1, 4.0)

    def test_convert_to_dict(self):
        entry = Entry("Yahoo News - Latest News & Headlines", "Title 1", "Wed, 06 Nov 2019 14:22:10 +0500",
                      "https://link1.com", "summary", ("https://link1.com",))
        entry.publish_year = 2019
        entry.publish_month = 12
        entry.publish_day = 11
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertEqual(entry_dict, self.handler.convert_Entry_to_dict(entry))

    def test_convert_to_dict_fail(self):
        entry = Entry("Yahoo News - Latest News & Headlines", "Title 15", "Wed, 06 Nov 2019 14:22:10 +0500",
                      "https://link1.com", "summary", ("https://link1.com",))
        entry.publish_year = 2019
        entry.publish_month = 12
        entry.publish_day = 11
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertNotEqual(self.handler.convert_Entry_to_dict(entry), entry_dict)

    def test_get_entry_from_dict_instance(self):
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019 14:22:10 +0500",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertIsInstance(self.handler.get_entry_from_dict(entry_dict), Entry)

    def test_get_entry_from_dict_not_instance(self):
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019 14:22:10 +0500",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        self.assertNotIsInstance(self.handler.get_entry_from_dict(entry_dict), Handler)

    def test_option_date_exc(self):
        self.assertRaises(RSSReaderException, lambda: self.handler.option_date("19950514", False, False, ""))

    def test_print_entry(self):
        expected_entry = 'Feed: feed\n\nTitle: title\nDate: Wed, 20 Nov 2019\nLink: link\n\n' \
                         'some_text\n\nLinks:\n[0] article_link (link)\n[1] img_link (image)\n\n\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            entry = Entry(feed="feed", title="title", date="Wed, 20 Nov 2019", article_link="link",
                          summary="some_text", links=("article_link", "img_link"))
            self.handler.print_entry(entry)
            self.assertEqual(expected_entry, fake_out.getvalue())

    def test_print_to_json(self):
        expected_json = '{\n  "Feed": "Yahoo News - Latest News & Headlines",\n  "Title": "Title 1",' \
                        '\n  "DateInt": "20191211",\n  "Date": "Wed, 06 Nov 2019",' \
                        '\n  "Link": "https://link1.com",\n  "Summary": "summary",\n  "Links": [\n    "https://link1.com"\n  ]\n}\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            entry_dict = dict(Feed="Yahoo News - Latest News & Headlines", Title="Title 1", DateInt="20191211",
                              Date="Wed, 06 Nov 2019", Link="https://link1.com", Summary="summary",
                              Links=("https://link1.com",))
            self.handler.print_to_json(entry_dict)
            self.assertEqual(expected_json, fake_out.getvalue())

    def test_correct_title(self):
        expected_corrected_title = "title_of_article_correct_ed"
        title = 'title?of:article correct"ed'
        self.assertEqual(expected_corrected_title, self.handler.correct_title(title))

    def test_write_cache(self):
        open_mock = mock_open()
        entry_dict = {
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019 14:22:10 +0500",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        }
        with patch("Handler.open", open_mock, create=True):
            self.handler.write_cache(entry_dict)

        open_mock.assert_called_with("cache.json", "w")
        # the last record:
        open_mock.return_value.write.assert_called_with(']')

    def test_option_version(self):
        expected_output = 'version 4.0\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.handler.option_version()
            self.assertEqual(expected_output, fake_out.getvalue())

    def test_option_json(self):
        self.handler.write_cache = MagicMock(return_value=True)
        self.assertEqual(True, self.handler.write_cache())
        entry = Entry(feed="feed", title="title", date="Wed, 20 Nov 2019", article_link="link",
                      summary="some_text", links=("article_link", "img_link"))
        self.handler.entries = [entry]
        self.handler.convert_Entry_to_dict = MagicMock(return_value={
            "Feed": "Yahoo News - Latest News & Headlines",
            "Title": "Title 1",
            "DateInt": "20191211",
            "Date": "Wed, 06 Nov 2019",
            "Link": "https://link1.com",
            "Summary": "summary",
            "Links": ("https://link1.com",)
        })
        expected_json = '{\n  "Feed": "Yahoo News - Latest News & Headlines",\n  "Title": "Title 1",' \
                        '\n  "DateInt": "20191211",\n  "Date": "Wed, 06 Nov 2019",' \
                        '\n  "Link": "https://link1.com",\n  "Summary": "summary",\n  "Links": [\n  ' \
                        '  "https://link1.com"\n  ]\n}\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.handler.option_json()
            self.assertEqual(expected_json, fake_out.getvalue())

    def test_write_entries_to_html(self):
        open_mock = mock_open()
        entry = Entry(feed="feed", title="title", date="Wed, 20 Nov 2019", article_link="link",
                      summary=" []some_text", links=("article_link", "img_link"))
        with patch("Handler.open", open_mock, create=True):
            self.handler.write_entries_to_html(os.path.abspath(os.path.dirname(__file__)), (entry,))

        open_mock.assert_called_with(f"{os.path.abspath(os.path.dirname(__file__))}\\RSS_News.html", "w", encoding='utf-8')
        open_mock.return_value.write.assert_called_once()
        open_mock.return_value.write.assert_called_once_with(
            '<html>\n  <head>\n    <meta charset="utf-8">\n  </head>\n  <body>\n    <div>\n      <h1>title</h1>'
            '\n      <p>\n        <b>Feed: </b>\n        <a>feed</a>\n      </p>\n      <p>\n        <b>Date: </b>\n'
            '        <a>Wed, 20 Nov 2019</a>\n      </p>\n      <img src="file:///F:\\Introduction to Python'
            '\\Final Task\\FinalTaskRssParser\\final_task\\rss_reader\\tests/images/title0.jpg"><br><br>\n      '
            '<p>some_text<br><br></p>\n    </div>\n  </body>\n</html>')

    def test_write_entries_to_html_without_img(self):
        open_mock = mock_open()
        entry = Entry(feed="feed", title="title", date="Wed, 20 Nov 2019", article_link="link",
                      summary=" []some_text", links=("article_link",))
        with patch("Handler.open", open_mock, create=True):
            self.handler.write_entries_to_html(os.path.abspath(os.path.dirname(__file__)), (entry,))

        open_mock.assert_called_with(f"{os.path.abspath(os.path.dirname(__file__))}\\RSS_News.html", "w", encoding='utf-8')
        open_mock.return_value.write.assert_called_once()
        open_mock.return_value.write.assert_called_once_with(
            '<html>\n  <head>\n    <meta charset="utf-8">\n  </head>\n  <body>\n    <div>\n      <h1>title</h1>\n      '
            '<p>\n        <b>Feed: </b>\n        <a>feed</a>\n      </p>\n      <p>\n        <b>Date: </b>\n        '
            '<a>Wed, 20 Nov 2019</a>\n      </p>\n      <p>some_text<br><br></p>\n    </div>\n  </body>\n</html>')

    def test_write_entries_to_pdf(self):
        open_mock = mock_open()
        entry = Entry(feed="feed", title="title", date="Wed, 20 Nov 2019", article_link="link",
                      summary=" []some_text", links=("article_link", "img_link"))
        with patch("Handler.open", open_mock, create=True):
            self.handler.write_entries_to_pdf(os.path.abspath(os.path.dirname(__file__)), (entry,))
        self.assertRaises(RSSReaderException,
                          lambda: self.handler.write_entries_to_pdf(os.path.abspath(__file__), (entry,)))

    def test_option_date(self):
        self.assertRaises(RSSReaderException,
                          lambda: self.handler.option_date("20191411", True, "path_html", "path_pdf"))
        self.handler.write_entries_to_pdf = MagicMock(return_value=True)
        self.handler.write_entries_to_html = MagicMock(return_value=True)
        self.handler.print_to_json = MagicMock(return_value=True)
        self.handler.get_entry_from_dict = MagicMock(return_value=True)
        self.handler.print_entry = MagicMock(return_value=True)
        self.handler.option_date("20191111", True, "path_html", "path_pdf")
        self.handler.option_date("20191111", False)
        # self.assertEqual(True, self.handler.option_date("20191111", True, "path_html", "path_pdf"))


if __name__ == '__main__':
    unittest.main()
