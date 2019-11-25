import unittest
from output_functions import getting_info_into_file
from Classes.novelty import Novelty


class GetInfo(unittest.TestCase):
    def test_getting_not_correct_item(self):
        item = Novelty(1, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        novelty = f"\n{1}.\nTitle: {'a'}\nDate: {'b'}\nLink: {'c'}\nDescription:\n {'d'}\nImages links:{'e'}\n" \
                  f"Alternative text:{'f'}\n Main source: {'h'}"
        self.assertNotEqual(getting_info_into_file(item), novelty, 'Should be')

    def test_getting_correct_item(self):
        item = Novelty(1, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        novelty = f"\n{1}.\nTitle: '{'a'}'\nDate: {'b'}\nLink: '{'c'}'\nDescription:\n '{'d'}'\n" \
                  f"Images links:'{'e'}'\nAlternative text:'{'f'}'\n Main source: {'h'}"
        print(novelty)
        print(getting_info_into_file(item))
        self.assertRaises(AssertionError and TypeError, getting_info_into_file(item), novelty)


if __name__ == '__main__':
    unittest.main()
