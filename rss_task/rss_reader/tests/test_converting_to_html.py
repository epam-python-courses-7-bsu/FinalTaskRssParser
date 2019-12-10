import unittest
from pdf_and_html_converting import converting_to_html
from pathlib import Path
from Classes.novelty import Novelty


class ToHtml(unittest.TestCase):
    def test_right(self):
        self.assertIsNone(converting_to_html(Path("bla-bla"), [Novelty(1, 'Title of', 'Date of', 'Link', 'Descript',
                                                                       'http://l1.yimg.com/uu/api/res/1.2'
                                                                       '/ksVTE6rKNuLy29FWWowIRw'
                                                                       '--/YXBwaWQ9eXRhY2h5b247aD04Njt3'
                                                                       'PTEzMDs-/https://media'
                                                                       '.zenfs.com/en/the_independent_6'
                                                                       '35/0928c8eca47092b771dabf2f16e88ed4',
                                                                       'fdfd',
                                                                       'g', 'h')]))

    def test_not_full_info(self):
        self.assertIsNone(converting_to_html(Path("bla-bla"), [Novelty(1, '', 'b', '', 'd', 'e', '', 'g', 'h')]))


if __name__ == '__main__':
    unittest.main()
