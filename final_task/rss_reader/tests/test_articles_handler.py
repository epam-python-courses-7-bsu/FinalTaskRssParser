"""Module for testing articles_handler"""
import dataclasses
import unittest
from unittest.mock import patch, MagicMock

import feedparser

import articles_handler
import custom_error
import single_article
import io


class TestArticlesHandler(unittest.TestCase):
    """Tests article_handler"""

    def setUp(self) -> None:
        self.first_article = single_article.SingleArticle(feed='Yahoo News',
                                                          feed_url='https://www.yahoo.com/news',
                                                          title='House Democrats',
                                                          date='Wed, 20 Nov 2019 20:54:24 -0500',
                                                          link='https://news.yahoo.com/democrats.html',
                                                          summary='Some text here1',
                                                          links=[['http://l2.yimg.com/10a59', 'image'],
                                                                 ['https://news.yahoo.com/democrats.html', 'other']])

        self.second_article = single_article.SingleArticle(feed='Yahoo News',
                                                           feed_url='https://www.yahoo.com/news',
                                                           title='Trump',
                                                           date='Fri, 22 Nov 2019 10:36:29 -0500',
                                                           link='https://news.yahoo.com/trump.html',
                                                           summary='Some text here1',
                                                           links=[['http://l2.yimg.com/uu/', 'image'],
                                                                  ['https://news.yahoo.com/trump.html', 'other']])

    def test_create_rss_json(self):
        """Testing json convertion"""
        expected_return = str([dataclasses.asdict(self.first_article)]).replace("'", '"')
        self.assertEqual(articles_handler.create_rss_json([self.first_article]), expected_return)

    def test_print_article(self):
        """Testing article print"""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            articles_handler.print_article(self.first_article)
            expected_out = str(f"{'-' * 120}\n{self.first_article}\n{'-' * 120}\n")

            self.assertEqual(fake_out.getvalue(), expected_out)

    def test_print_rss_articles(self):
        """Testing all articles print"""
        expected_out = str(f"{'-' * 120}\n{self.first_article}\n{'-' * 120}\n" +
                           f"{'-' * 120}\n{self.second_article}\n{'-' * 120}\n")
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            articles_handler.print_rss_articles([self.first_article, self.second_article])

            self.assertEqual(fake_out.getvalue(), expected_out)

    def test_find_links_in_article(self):
        """Testing the search for links in the text with/without alt,src"""
        summary_with_src_and_alt = '<p><a href="https://test.site.com/1.html"><img src="http://img.com/img.jpg" ' \
                                   'width="130" height="86" alt="Image alt" align="left" title="title text" ' \
                                   'border="0" ></a>ARTICLE TEXT<p><br clear="all">'

        test_article_dict = {'summary': summary_with_src_and_alt,
                             'links': [{'href': 'https://testlink1.html'},
                                       {'href': 'https://testlink2.html"'}]}

        expected_result = ([['http://img.com/img.jpg', 'image'],
                            ['https://testlink1.html', 'other'],
                            ['https://testlink2.html"', 'other']],
                           '[image 1: Image alt][1] ARTICLE TEXT')

        entry = MagicMock(spec=feedparser.FeedParserDict)
        entry.__getitem__.side_effect = test_article_dict.__getitem__

        self.assertEqual(articles_handler.find_links_in_article(entry), expected_result)

        summary_with_no_alt = '<p><a href="https://test.site.com/1.html"><img src="http://img.com/img.jpg"' \
                              ' width="130" height="86" alt="" align="left" title="title text" border="0" >' \
                              '</a>ARTICLE TEXT<p><br clear="all">'

        test_article_dict['summary'] = summary_with_no_alt

        expected_result = ([['http://img.com/img.jpg', 'image'],
                            ['https://testlink1.html', 'other'],
                            ['https://testlink2.html"', 'other']],
                           '[image 1: no description][1] ARTICLE TEXT')

        self.assertEqual(articles_handler.find_links_in_article(entry), expected_result)

        summary_with_no_src = '<p><a href="https://test.site.com/1.html"><img src="" ' \
                              'width="130" height="86" alt="Image alt" align="left" title="title text" ' \
                              'border="0" ></a>ARTICLE TEXT<p><br clear="all">'

        test_article_dict['summary'] = summary_with_no_src

        expected_result = ([['https://testlink1.html', 'other'],
                            ['https://testlink2.html"', 'other']],
                           '[image(no link): Image alt] ARTICLE TEXT')

        self.assertEqual(articles_handler.find_links_in_article(entry), expected_result)

        summary_with_no_src_no_alt = '<p><a href="https://test.site.com/1.html"><img src=""' \
                                     ' width="130" height="86" alt="" align="left" title="title text" border="0" >' \
                                     '</a>ARTICLE TEXT<p><br clear="all">'

        test_article_dict['summary'] = summary_with_no_src_no_alt

        expected_result = ([['https://testlink1.html', 'other'],
                            ['https://testlink2.html"', 'other']],
                           'ARTICLE TEXT')

        self.assertEqual(articles_handler.find_links_in_article(entry), expected_result)

        summary_with_two_img = '<p><a href="https://test1.com/1.html"><img src="http://img.com/img.jpg" ' \
                               'width="130" height="86" alt="Image1 alt" align="left" title="title text" ' \
                               'border="0" ><a href="https://test2.com/1.html"><img src="http://img2.com/img.jpg" ' \
                               'width="130" height="86" alt="Image2 alt" align="left" title="title text" ' \
                               'border="0" ></a>ARTICLE TEXT<p><br clear="all">'

        test_article_dict['summary'] = summary_with_two_img

        expected_result = ([['http://img.com/img.jpg', 'image'],
                            ['http://img2.com/img.jpg', 'image'],
                            ['https://testlink1.html', 'other'],
                            ['https://testlink2.html"', 'other']],
                           '[image 1: Image1 alt][1] [image 2: Image2 alt][2] ARTICLE TEXT')

        self.assertEqual(articles_handler.find_links_in_article(entry), expected_result)

        summary_with_no_img = '<p><a href="https://test1.com/1.html"></a>ARTICLE TEXT<p><br clear="all">'

        test_article_dict['summary'] = summary_with_no_img

        expected_result = ([['https://testlink1.html', 'other'],
                            ['https://testlink2.html"', 'other']],
                           'ARTICLE TEXT')

        self.assertEqual(articles_handler.find_links_in_article(entry), expected_result)

        test_article_dict['summary'] = 'Text'
        test_article_dict['links'] = ''
        expected_result = ([], 'Text')

        self.assertEqual(articles_handler.find_links_in_article(entry), expected_result)

    def test_unescape(self):
        """Testing unescape work"""
        text_to_test = '“by means of arrest,&quot; and he won&#39;t testify inquiry, writes Daniel S. Alter.'
        expected_result = "“by means of arrest,\" and he won't testify inquiry, writes Daniel S. Alter."
        self.assertEqual(articles_handler.unescape(text_to_test), expected_result)

    @patch('articles_handler.find_links_in_article')
    def test_get_articles(self, mock_links):
        """Testing conversion FeedParserDict with articles to list with SingleArticle"""
        test_articles_dict = {'feed': {'title': 'Yahoo',
                                       'title_detail': {'base': 'https://www.yahoo.com/news'}},
                              'entries': [{'title': 'Article1',
                                           'published': 'date',
                                           'link': 'link1'},
                                          {'title': 'Article2',
                                           'published': 'date',
                                           'link': 'link2'}]}

        links_return = [([['http://img.com/img1.jpg', 'image'], ['https://testlink1.html', 'other']],
                         '[image 1: Image alt][1] ARTICLE 1 TEXT'),
                        ([['http://img.com/img2.jpg', 'image'], ['https://testlink2.html', 'other']],
                         '[image 1: Image alt][1] ARTICLE 2 TEXT')]
        mock_links.side_effect = links_return

        articles = MagicMock(spec=feedparser.FeedParserDict)
        articles.__getitem__.side_effect = test_articles_dict.__getitem__

        expected_result = [single_article.SingleArticle(feed='Yahoo',
                                                        feed_url='https://www.yahoo.com/news',
                                                        title='Article1', date='date',
                                                        link='link1',
                                                        summary='[image 1: Image alt][1] ARTICLE 1 TEXT',
                                                        links=[['http://img.com/img1.jpg', 'image'],
                                                               ['https://testlink1.html', 'other']]),
                           single_article.SingleArticle(feed='Yahoo', feed_url='https://www.yahoo.com/news',
                                                        title='Article2', date='date', link='link2',
                                                        summary='[image 1: Image alt][1] ARTICLE 2 TEXT',
                                                        links=[['http://img.com/img2.jpg', 'image'],
                                                               ['https://testlink2.html', 'other']])]

        self.assertEqual(articles_handler.get_articles(articles, None), expected_result)

        links_return += ([['http://img.com/img3.jpg', 'image'], ['https://testlink3.html', 'other']],
                         '[image 1: Image alt][1] ARTICLE 3 TEXT')

        mock_links.side_effect = links_return

        with self.assertRaises(custom_error.ArticleKeyError):
            test_articles_dict['entries'].append({'published': 'date',
                                                  'link': 'link2'})
            articles_handler.get_articles(articles, None)

    def test_convert_dict_to_single_article(self):
        """Testing conversion"""
        self.assertEqual(articles_handler.convert_dict_to_single_article(dataclasses.asdict(self.first_article)),
                         self.first_article)
        self.assertEqual(articles_handler.convert_dict_to_single_article(dataclasses.asdict(self.second_article)),
                         self.second_article)


if __name__ == '__main__':
    unittest.main()
