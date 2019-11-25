#!/usr/bin/env python3.8
"""Module for testing pdf_converter.py"""

import unittest
from unittest.mock import patch, MagicMock

import pdf_converter


class TestAddDownloaderImage(unittest.TestCase):
    """
    Test function from pdf_converter.py
    """

    @patch('pdf_converter.add_image_link')
    @patch('os.remove')
    @patch('urllib.request.urlretrieve')
    def test_add_downloaded_image_not_jpeg_png(self, urlretrieve, remove, add_image_link):
        """
        Test add_downloaded_image(num, link, pdf) if image format isn't jpeg or png
        """
        num, link = 1, 'link'
        pdf = MagicMock()
        urlretrieve.return_value = ('filename', {'content-type': 'image/'})

        self.assertEqual(None, pdf_converter.add_downloaded_image(num, link, pdf))

        pdf.image.assert_not_called()
        pdf.ln.assert_not_called()
        add_image_link.assert_called_once_with(num, link, pdf)
        remove.assert_not_called()

    @patch('pdf_converter.add_image_link')
    @patch('os.remove')
    @patch('urllib.request.urlretrieve')
    def test_add_downloaded_image_jpeg_or_png(self, urlretrieve, remove, add_img_link):
        """
        Test add_downloaded_image(num, link, pdf) if image format is jpeg or png
        """
        num, link = 1, 'link'
        pdf = MagicMock()
        urlretrieve.return_value = ('filename', {'content-type': 'image/jpeg'})

        self.assertEqual(None, pdf_converter.add_downloaded_image(num, link, pdf))

        pdf.image.assert_called_once()
        pdf.ln.assert_called_once_with(40)
        remove.assert_called_once_with('filename')
        add_img_link.assert_not_called()


if __name__ == '__main__':
    unittest.main()
