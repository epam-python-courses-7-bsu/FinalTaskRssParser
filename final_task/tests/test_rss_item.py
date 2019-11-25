import sys
import unittest
from colorama import Fore, Back, Style, init
from io import StringIO
from unittest.mock import patch

sys.path.insert(1, 'final_task/rss_reader')
from rss_item import RssItem
init()


class TestRssItem(unittest.TestCase):

    def setUp(self):
        self.item = RssItem('title', 'date', 'description', 'link', 'media', 'source', 'date_parsed', 'base64 image')

    def test_string(self):
        expected_result = 'TITLE: ' + Back.BLACK + Fore.WHITE + 'title' + Style.RESET_ALL\
            + '            \n\t|| DESCRIPTION: ' + Fore.MAGENTA + 'description' + Fore.RESET\
            + '            \n\t|| PUBLISHED: ' + Fore.GREEN + 'date' + Fore.RESET\
            + '            \n\t|| LINK: ' + Fore.BLUE + 'link' + Fore.RESET\
            + '            \n\t|| MEDIA: ' + Fore.YELLOW + 'media' + Fore.RESET
        self.assertEqual(self.item.__str__(), expected_result)

    def test_to_json(self):
        expected_result = '{\n'\
            '    "date": "date_parsed",\n'\
            '    "description": "description",\n'\
            '    "img": "base64 image",\n'\
            '    "link": "link",\n'\
            '    "media": "media",\n'\
            '    "published": "date",\n'\
            '    "source": "source",\n'\
            '    "title": "title"\n'\
            '}\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.item.to_json()
            self.assertEqual(fake_out.getvalue(), expected_result)
