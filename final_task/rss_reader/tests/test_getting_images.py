import unittest
from pdf_and_html_converting import getting_images
from Classes.novelty import Novelty
from pathlib import Path
import os


class GetImages(unittest.TestCase):
    def test_wrong(self):
        self.assertRaises(TypeError, getting_images(Path("bla-bla"), [Novelty(1, 'a', 'b', 'c', 'd',
                                                                              'http://l1.yimg.com/uu/api/res/1.2'
                                                                              '/ksVTE6rKNuLy29FWWowIRw'
                                                                              '--/YXBwaWQ9eXRhY2h5b247aD04Njt3'
                                                                              'PTEzMDs-/https://media'
                                                                              '.zenfs.com/en/the_independent_6'
                                                                              '35/0928c8eca47092b771dabf2f16e88ed4',
                                                                              'f',
                                                                              'g', 'h')]))

    def test_assert(self):
        self.assertRaises(TypeError, getting_images(Path(os.curdir), [Novelty(1, 'a', 'b', 'c', 'd',
                                                                              'http://l1.yimg.com/uu/api/res/1.2'
                                                                              '/ksVTE6rKNuLy29FWWowIRw'
                                                                              '--/YXBwaWQ9eXRhY2h5b247aD04Njt3'
                                                                              'PTEzMDs-/https://media'
                                                                              '.zenfs.com/en/the_independent_6'
                                                                              '35/0928c8eca47092b771dabf2f16e88ed4',
                                                                              'f',
                                                                              'g', 'h')]))


if __name__ == '__main__':
    unittest.main()
