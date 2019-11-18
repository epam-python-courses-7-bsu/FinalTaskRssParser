import unittest
import json
import sys
import copy
sys.path.append('../rss_reader')
from NewsCache import NewsCache

TEST_NEWS_LIST = [
            {"Title": "Air racing tournament unveils an all-electric sports aircraft",
             "Date": "Sun, 17 Nov 2019 15:35:00 -0500",
             "Link": "link",
             "Summary": "Test text",
             "Image": "\nSource of image: img_link",
             "Date key": "20191117"}]

FILE_CONTENTS = {"20191117":
    {"https://www.engadget.com/rss.xml":
        {"Air racing tournament unveils an all-electric sports aircraft":
            {"Title": "Air racing tournament unveils an all-electric sports aircraft",
             "Date": "Sun, 17 Nov 2019 15:35:00 -0500",
             "Link": "link",
             "Summary": "Test text",
             "Image": "\nSource of image: img_link"}}}}


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.cache = NewsCache('Test_file.json')
        test_news = copy.deepcopy(TEST_NEWS_LIST)
        self.cache.caching(test_news, 'https://www.engadget.com/rss.xml')

    def test_caching(self):
        with open('Test_file.json', "r") as test_json:
            content = test_json.read()
            self.assertEqual(json.loads(content), FILE_CONTENTS)
            self.assertEqual(json.loads(content).get('20191117'), FILE_CONTENTS['20191117'])

    def test_returning(self):
        result = self.cache.returning('20191117', 'https://www.engadget.com/rss.xml')
        self.assertEqual(result[0].get('Title'), "Air racing tournament unveils an all-electric sports aircraft")
        self.assertEqual(result[0].get('Date'), "Sun, 17 Nov 2019 15:35:00 -0500")
        self.assertEqual(result[0].get('Link'), "link")
        self.assertEqual(result[0].get('Summary'), "Test text")
        self.assertEqual(result[0].get('Image'), "\nSource of image: img_link")


if __name__ == '__main__':
    unittest.main()
