import sys
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(1, 'final_task/rss_reader')
from rss_reader import init_feed, init_news_list, extract_text_from_html, get_img_base64
from rss_item import RssItem


class TestRssReader(unittest.TestCase):

    def test_init_feed(self):
        news_feed = init_feed('final_task/tests/test_feed.xml', 2)
        rss_items = [
            RssItem('ITEM1 TITLE', '2003-12-31', 'unknown', 'ITEM1 LINK',
                    'http://www.foo.com/bar.jpg', 'final_task/tests/test_feed.xml', '20031231', 'b\'bm90IGZvdW5k\''),

            RssItem('ITEM2 TITLE', '2003-12-31', 'unknown', 'ITEM2 LINK',
                    'http://www.foo.com/bar.jpg', 'final_task/tests/test_feed.xml', '20031231', 'b\'bm90IGZvdW5k\'')
            ]
        self.assertEqual(news_feed.title, 'CHANNEL TITLE')
        self.assertEqual(news_feed.description, 'CHANNEL DESCRIPTION')
        self.assertEqual(news_feed.link, 'CHANNEL LINK')
        self.assertEqual(news_feed.news_list, rss_items)

    def test_extract_text_from_html(self):
        input_html = '<p><a href="https://news.yahoo.com/booker-and-harris-warn-'\
            'dems-electability-doesnt-just-mean-appealing-to-white-voters-2118201'\
            '55.html"><img src="http://l.yimg.com/uu/api/res/1.2/zvyOlzJsHCTtl3Oi'\
            'CruwkA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub'\
            '-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/16313810-0c9b-1'\
            '1ea-a7db-c5ca01aa642b" width="130" height="86" alt="Booker and Harri'\
            's warn Dems: Electability doesn&#39;t just mean appealing to white v'\
            'oters" align="left" title="Booker and Harris warn Dems: Electability'\
            ' doesn&#39;t just mean appealing to white voters" border="0" ></a>El'\
            'ectability is the biggest buzzword of the 2020 cycle. It’s what Dem'\
            'ocrats say they prize above all else: a nominee who can defeat Dona'\
            'ld Trump. But it&#39;s also a code word. It tends to mask a raciali'\
            'zed assumption about which Americans a candidate needs to win over '\
            'in order to qualify as “electable”: that is, white voters who don’t'\
            ' live in big coastal cities.<p><br clear="all">'
        expected_result = 'Electability is the biggest buzzword of the 2020 cycl'\
            'e. It’s what Democrats say they prize above all else: a nominee who '\
            'can defeat Donald Trump. But it\'s also a code word. It tends to mas'\
            'k a racialized assumption about which Americans a candidate needs to'\
            ' win over in order to qualify as “electable”: that is, white voters '\
            'who don’t live in big coastal cities.'
        result = extract_text_from_html(input_html)
        self.assertEqual(result, expected_result)

    def test_get_img_base64(self):
        url = 'https://docs.python.org/2/_static/py.png'
        expected_result = 'b\'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR'\
            '0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0'\
            'SU1FB9gEGxE4IQYzJ14AAAI3SURBVDjLZZNPSFVBFIe/e9+zd3silBCl0SZoU4s2rVq'\
            '0EB5tQip4UNvATVGu3QRBiyAi2iltWkgbF5EgRhFFRpiWtrWIzDIV1Pzz7p15M2fmtv'\
            'DevOqBw8DM9zvnN8ycgF3R/eDtM2mac96ZdrFNxBikqbRV+vHH/ut9gAZczoe7C3gnF'\
            '0f6au1OLM5avFi8d1Ea+JvAMSAq8nsKOGs5f2cYJ3Y7rc2PO4BqkS8DdD98f9tbe1ys'\
            'CoxOBo1qlEXHJWcM4b5KPU19zleA0o4Clx99eO3EdqVewHsCoFRugUoVghJO7A6H6Vx'\
            '9wdtYi27cr5x6dy/03nVtWTU7bWeZh6jNUcAiCaFTURl9A+gs56AviHzh3mnqtdPxm6'\
            'knfQPLU7UaokASQq/agY7yDrG16Mba6Pz48NP56VdrgAApYObGaicPtkovToFLQBKA/'\
            'WUxTe3FRk4san15aGKgd3Dj560rrdGJS6FT0X9YYvLuiMKL1kAQOpHZ3PqfyZfP41+9'\
            'PW1VfzX0RXFSECfgNEmSTgImdDruF2O0E8vvqZG1auQubAsKooIYYHpGvwA2g+xndQB'\
            'HgWa6cG0ih5cW/w6VvEq3nChwCoBvs+bL2Z7VceBHGTDAIrABpMVuhw+4OiLgLIglOL'\
            'PYBTQAlfErIeCzjRVg1dtEb1kt5Omv+DTV2YssAN+zNdkzC42N9brV8WdvYp07seOdM'\
            '2Of1F3AAknW0AJpwN6IgEPAEaANaMlcbmZdl7KRBuAfAb+v//yMAJoAAAAASUVORK5CYII=\''
        result = get_img_base64(url)
        self.assertEqual(result, expected_result)
        wrong_url_result = get_img_base64('blablabla')
        self.assertEqual(wrong_url_result, 'no image')
