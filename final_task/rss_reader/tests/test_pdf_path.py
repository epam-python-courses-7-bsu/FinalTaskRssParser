import unittest
from pdf_and_html_converting import pdf_path
from pathlib import Path


class PathPdf(unittest.TestCase):
    def test_correct_path(self):
        list_of_args = ['--to-pdf', 'C:\\Directory\\']
        self.assertEqual(pdf_path(list_of_args), Path('C:\\Directory\\'))

    def test_not_correct_path(self):
        list_of_args = ['--to-pdf', 'ABC:><>//Dir\\']
        self.assertRaises(TypeError, pdf_path(list_of_args), 'A')


if __name__ == '__main__':
    unittest.main()
