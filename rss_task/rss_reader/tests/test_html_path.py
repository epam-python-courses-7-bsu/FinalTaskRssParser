import unittest
from pdf_and_html_converting import html_path
from pathlib import Path


class PathHtml(unittest.TestCase):
    def test_correct_path(self):
        list_of_args = ['--to-html', 'C:\\Directory\\']
        self.assertEqual(html_path(list_of_args), Path('C:\\Directory\\'))

    def test_not_correct_path(self):
        list_of_args = ['--to-html', 'ABC:><>//Dir\\']
        self.assertRaises(TypeError, html_path(list_of_args), 'A')


if __name__ == '__main__':
    unittest.main()
