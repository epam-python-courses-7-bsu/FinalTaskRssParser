import unittest
import tools


class TestTools(unittest.TestCase):
    def test_merge_lists(self):
        list0 = [1, 3, 11, 27]
        list1 = [100, 3, 2, 11, 77]
        list2 = [3, 11, 1, 27]
        list3 = []
        list4 = [7, 8, 9]

        self.assertEqual(tools.merge_lists(list0, list1), [1, 3, 11, 27, 100, 2, 77])
        self.assertEqual(tools.merge_lists(list0, list2), [1, 3, 11, 27])
        self.assertEqual(tools.merge_lists(list0, list3), [1, 3, 11, 27])
        self.assertEqual(tools.merge_lists(list0, list4), [1, 3, 11, 27, 7, 8, 9])


if __name__ == '__main__':
    unittest.main()
