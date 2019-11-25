import unittest
from unittest.mock import patch, call

import exceptions
from news_articles import NewsArticle
from converter import converter, convert_to_html, save_html, save_pdf


class TestConverter(unittest.TestCase):

    def setUp(self):
        self.news_article_1 = NewsArticle(news_outlett_name='Yahoo News',
                                          news_title='OK Boomer',
                                          pub_date='Fri, 22 Nov 2019 15:47:25 -0500',
                                          news_link='news link',
                                          news_description='A long news description',
                                          img_alt='Smile sunshine',
                                          img_src='IMG link')
        self.news_article_2 = NewsArticle(news_outlett_name='Yahoo',
                                          news_title='Boomer',
                                          pub_date='Fri, 22 Nov 2019 15:47:25 -0500',
                                          news_link='link',
                                          news_description='A description',
                                          img_alt='Smile',
                                          img_src='IMG link')
        self.path_to_html = 'funny'
        self.path_to_pdf = 'boring'
        self.news_articles = [self.news_article_1, self.news_article_2]
        self.pseudo_html_code = 'I am not html'

    def test_converter(self):
        with patch('converter.convert_to_html') as mocked_convert_to_html:
            converter(self.news_articles, None, None)
            mocked_convert_to_html.assert_called_with(self.news_articles)
            # if path_to_html is provided -> call save_html
            with patch('converter.save_html') as mocked_save_html:
                converter(self.news_articles, self.path_to_html, None)
                mocked_save_html.assert_called_with(mocked_convert_to_html(), self.path_to_html)
            # if path_to_pdf is provided -> call save_pdf
            with patch('converter.save_pdf') as mocked_save_pdf:
                converter(self.news_articles, None, self.path_to_pdf)
                mocked_save_pdf.assert_called_with(mocked_convert_to_html(), self.path_to_pdf)

    def test_convert_to_html(self):
        self.assertRaises(exceptions.NoDataToConvertError, convert_to_html, [])
        with patch('converter.Environment.get_template') as mocked_get_template:
            convert_to_html(self.news_articles)
            mocked_get_template.assert_called_with('template.html')
            mocked_get_template().render.assert_called_with(news_articles=self.news_articles)

    def test_save_html(self):
        with patch('builtins.open') as mocked_open:
            save_html(self.pseudo_html_code, self.path_to_html)
            mocked_open.assert_called_with(f'{self.path_to_html}.html', 'w')
            assert call().__enter__().writelines(self.pseudo_html_code) in mocked_open.mock_calls

    def test_save_pdf(self):
        with patch('weasyprint.HTML') as mocked_weasy:
            save_pdf(self.pseudo_html_code, self.path_to_pdf)
            mocked_weasy.assert_called_with(string=self.pseudo_html_code)
            assert call().write_pdf(f'{self.path_to_pdf}.pdf') in mocked_weasy.mock_calls


if __name__ == "__main__":
    unittest.main()
