"""Module for testing colorizing_handler"""
import unittest
import colorizing_handler


class TestArticlesHandler(unittest.TestCase):
    """Tests colorizing_handler"""
    def test_set_colorizing_status(self):
        """Testing status set"""
        self.assertFalse(colorizing_handler.COLORIZING_STATUS)
        colorizing_handler.set_colorizing_status()
        self.assertTrue(colorizing_handler.COLORIZING_STATUS)


if __name__ == '__main__':
    unittest.main()
