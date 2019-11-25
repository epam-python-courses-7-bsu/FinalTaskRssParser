import unittest
from Classes.novelty import Novelty


class Novel(unittest.TestCase):
    def test_wrong_type(self):
        self.assertRaises(TypeError, Novelty('', '', '', '', '', '', '', '', ''))

    def test_all_right(self):
        self.assertTrue(Novelty(1, '', '', '', '', '', '', '', ''))


if __name__ == '__main__':
    unittest.main()
