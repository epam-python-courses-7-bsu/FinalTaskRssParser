import unittest
import sys
from unittest import mock
sys.path.append('../rss_reader')
from output import get_output_function, output, output_json, output_pdf, output_epub, parse_to_json


TEST_NEWS_LIST = [
            {"Title": "Some title",
             "Date": "Sun, 17 Nov 2019 15:35:00 -0500",
             "Link": "link",
             "Summary": "Test text",
             "Source of image": "img_link"}]


class OutputTestCase(unittest.TestCase):

    def test_get_output_function(self):
        result = get_output_function('text')
        self.assertEqual(result, output)
        result = get_output_function('json')
        self.assertEqual(result, output_json)
        result = get_output_function('pdf')
        self.assertEqual(result, output_pdf)
        result = get_output_function('epub')
        self.assertEqual(result, output_epub)

    def test_output(self):
        logger = mock.Mock()
        with mock.patch('sys.stdout') as mock_print:
            output(logger, TEST_NEWS_LIST)
            mock_print.assert_has_calls(
                [
                    mock.call.write('--------------------------------------------------------'),
                    mock.call.write('\n'),
                    mock.call.write("Title: Some title"),
                    mock.call.write('\n'),
                    mock.call.write("Date: Sun, 17 Nov 2019 15:35:00 -0500"),
                    mock.call.write('\n'),
                    mock.call.write("Link: link"),
                    mock.call.write('\n'),
                    mock.call.write("Summary: Test text"),
                    mock.call.write('\n'),
                    mock.call.write("Source of image: img_link"),
                    mock.call.write('\n'),
                ]
            )

    def test_output_json(self):
        logger = mock.Mock()
        with mock.patch('sys.stdout') as mock_print:
            output_json(logger, TEST_NEWS_LIST)
            mock_print.assert_has_calls(
                [
                    mock.call.write('[\n    '
                                    '{\n        "Title": "Some title",'
                                    '\n        "Date": "Sun, 17 Nov 2019 15:35:00 -0500",'
                                    '\n        "Link": "link",'
                                    '\n        "Summary": "Test text",'
                                    '\n        "Source of image": "img_link"'
                                    '\n    }'
                                    '\n]'),
                    mock.call.write('\n'),
                ]
            )


if __name__ == '__main__':
    unittest.main()
