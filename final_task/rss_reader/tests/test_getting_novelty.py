import unittest
from output_functions import getting_novelty
from Classes.novelty import Novelty


class GetNovelty(unittest.TestCase):
    def test_something(self):
        item = {'title': 'Title!',
                'published': 'Mon, 25 Nov 2019 06:02:00 -0500',
                'link': 'https://news.yahoo.com/donald-trump-chosen-one-sent-110225965.html',
                'description': 'DESCRIPTION...'}
        number = 0
        corrected_pack_of_alts = ['ALT', 'ALT']
        corrected_pack_of_images_links = ['LINK', 'LINK']
        main_source = 'https://news.yahoo.com/rss/'
        pack1, pack2 = getting_novelty(item, number, corrected_pack_of_images_links, corrected_pack_of_alts,
                                       main_source)
        self.assertEqual(pack1, Novelty(number_of_novelty=1, title_of_novelty='Title!',
                                        time_of_novelty='Mon, 25 Nov 2019 06:02:00 -0500',
                                        source_link='https://news.yahoo.com/donald-trump-chosen-one-sent-110225965.html',
                                        description='DESCRIPTION...', images_links='LINK', alt_text='ALT',
                                        date_corrected='20191125', main_source='https://news.yahoo.com/rss/'))
        self.assertEqual(pack2, (1, 'Title!', 'Mon, 25 Nov 2019 06:02:00 -0500',
                                 'https://news.yahoo.com/donald-trump-chosen-one-sent-110225965.html',
                                 'DESCRIPTION...', 'LINK', 'ALT', '20191125', 'https://news.yahoo.com/rss/'))


if __name__ == '__main__':
    unittest.main()
