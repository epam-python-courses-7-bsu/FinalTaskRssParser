from dateutil import parser
import sys

from News import News

sys.path.insert(1, 'final_task/rss_reader')
import converter
import unittest


class TestConverters(unittest.TestCase):
    def test_get_path(self):
        with self.assertRaises(FileNotFoundError) as error:
            converter.get_path('path_not_exist.txt', '.pdf')
        self.assertEqual(str(error.exception), 'Invalid expansion ')
        with self.assertRaises(FileNotFoundError) as error:
            converter.get_path('path_not_exist.pdf', '.pdf')
        self.assertEqual(str(error.exception), 'File or directory not found')
        with self.assertRaises(FileNotFoundError) as error:
            converter.get_path('path_not_exist.txt', '.html')
        self.assertEqual(str(error.exception), 'Invalid expansion ')
        with self.assertRaises(FileNotFoundError) as error:
            converter.get_path('path_not_exist.html', '.html')
        self.assertEqual(str(error.exception), 'File or directory not found')

    def test_get_img(self):
        self.assertEqual(converter.get_img("name", "not link"), False)
        self.assertEqual(converter.get_img('name', "https://news.tut.by/rss"), False)

    def test_text_separator(self):
        text = "A Utah woman charged with a crime after her stepchildren saw her topless in her own home is "
        result = ["A Utah woman charged with a crime after her",
                  "stepchildren saw her topless in her own home is"]
        self.assertEqual(converter.text_separator(text, False), result)

    def test_get_html(self):
        dat = parser.parse("2019-11-12 18:21:00+03:00")
        link12 = "link"
        link_on_image = "link on image"

        links1 = [link12, link_on_image]
        news = News(feed="TUT.BY: Новости ТУТ",
                    title="wcds",
                    date=dat,
                    link="link",
                    info_about_image="uhinjвв",
                    briefly_about_news="Полпред России в контактной группе Борис Грызлов сообщил",
                    links_from_news=links1)

        list_of_new = [news, ]
        verifiable_info = "<!DOCTYPE html>\n" \
                          "<html>\n" \
                          "  <head>\n" \
                          "    <title>RSS READER</title>\n" \
                          """    <link href="style.css" rel="stylesheet">\n""" \
                          """    <script src="script.js" type="text/javascript"></script>\n""" \
                          """    <style>                     body {\n""" \
                          """                         background-color: #F9F8F1;\n""" \
                          """                         color: #2C232A;\n""" \
                          """                         font-family: sans-serif;\n""" \
                          """                         font-size: 2.6em;\n""" \
                          """                         margin: 3em 1em;\n""" \
                          """                     }\n\n""" \
                          """                 </style>\n""" \
                          """  </head>\n""" \
                          """  <body>\n""" \
                          """    <div id="header">\n""" \
                          """      <p>Feed: TUT.BY: Новости ТУТ</p>\n""" \
                          """      <p>Title: wcds</p>\n""" \
                          """      <p>Date 2019-11-12 18:21:00+03:00</p>\n""" \
                          """      <p>Link: \n""" \
                          """        <a href="link" target="_blank">Link</a>\n""" \
                          """      </p>\n""" \
                          """      <p>Info about image: uhinjвв</p>\n""" \
                          """      <p>Briefly about news: Полпред России в контактной группе Борис Грызлов """ \
                          """сообщил</p>\n""" \
                          """      <p>Links: </p>\n""" \
                          """      <li>\n""" \
                          """        <a href="link" target="_blank">Link</a>\n""" \
                          """      </li>\n""" \
                          """      <li>\n""" \
                          """        <a href="link on image" target="_blank">Link On Image</a>\n""" \
                          """      </li>\n""" \
                          """      <a href="link on image" target="_blank">\n""" \
                          """        <img alt="uhinjвв" height="200" src="link on image" width="200">\n""" \
                          """      </a>\n""" \
                          """    </div>\n""" \
                          """  </body>\n""" \
                          """</html>"""

        document_of_html = converter.get_html(list_of_new)
        self.assertEqual(document_of_html.render(), verifiable_info)
