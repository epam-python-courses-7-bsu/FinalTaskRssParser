import unittest
from output_functions import getting_info_into_file
from Classes.novelty import Novelty


class GetInfo(unittest.TestCase):
    def test_getting_not_correct_item(self):
        item = Novelty(1, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        getting_info_into_file(item)
        a = 'a'
        novelty = f"\n{1}.\nTitle: {a}\nDate: {'b'}\nLink: {'c'}\nDescription:\n {'d'}\nImages links:{'e'}\n" \
                  f"Alternative text:{'f'}\n Main source: {'h'}"
        self.assertNotEqual(getting_info_into_file(item), novelty, 'Should be')


if __name__ == '__main__':
    unittest.main()
