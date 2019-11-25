import unittest
from output_functions import reading_file


class ReadFile(unittest.TestCase):
    def test_reading_equal(self):
        name_of_file = "test.txt"
        with open(name_of_file, 'w', encoding='utf-8') as news_cache:
            news_cache.write("Labu")

        self.assertEqual(reading_file('test.txt'), "Labu")


if __name__ == '__main__':
    unittest.main()
