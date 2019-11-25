import unittest
from output_functions import getting_corrected_time


class CorrectedTime(unittest.TestCase):
    def test_fine_format(self):
        time = {'published': 'Tue, 19 Nov 2019 19:12:56 -0500'}
        self.assertEqual(getting_corrected_time(time), '20191119')


if __name__ == '__main__':
    unittest.main()
