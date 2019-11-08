import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rss_reader'))
import work_with_text


class TestTextFunctions(unittest.TestCase):
    def test_get_img(self):
        entering = '<p><a href="https://news.yahoo.com/trump-fumes-washington-post-barr-press-conference-ukraine-call-' + \
                '145952187.html"><img src="http://l2.yimg.com/uu/api/res/1.2/fMm6_rzTShdBsnaYua7fIA--/YXBwaWQ9eXRhY' + \
                '2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11' + \
                '/e87f47a0-016d-11ea-ab5f-bdce0579bae9" width="130" height="86" alt="Trump fumes about reports that' + \
                ' he wanted Barr to host news conference clearing him on Ukraine call" align="left" title="Trump fu' + \
                'mes about reports that he wanted Barr to host news conference clearing him on Ukraine call" border' + \
                '="0" ></a>The president is lashing out on Twitter over news first reported by the Washington Post ' + \
                'that he wanted the attorney general to hold a press conference declaring he had broken no laws dur' + \
                'ing the July 25 phone call in which he urged Ukraine’s new president to investigate his political ' + \
                'rival.<p><br clear="all">'
        output = ['http://l2.yimg.com/uu/api/res/1.2/fMm6_rzTShdBsnaYua7fIA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs' +
                  '-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/e87f47a0-016d-11e' +
                  'a-ab5f-bdce0579bae9', 'Trump fumes about reports that he wanted Barr to host news conference c' +
                  'learing him on Ukraine call']
        self.assertEqual(work_with_text.get_img(entering), output)

        entering = '<img src="link" alt="alt">'
        output = ['link', 'alt']
        self.assertEqual(work_with_text.get_img(entering), output)

        entering = '<img src="link" alt="alt">'
        output = ['links', 'alt']
        self.assertNotEqual(work_with_text.get_img(entering), output)

    def test_text_processing(self):
        links = []
        entering = 'test'
        output = 'test'
        self.assertEqual(work_with_text.text_processing(entering, links), output)

        entering = 'test_'
        output = 'test'
        self.assertNotEqual(work_with_text.text_processing(entering, links), output)

        entering = '<p>test'
        output = 'test'
        self.assertEqual(work_with_text.text_processing(entering, links), output)

        entering = '<>test<>'
        output = 'test'
        self.assertEqual(work_with_text.text_processing(entering, links), output)

        entering = '<img src="link" alt="text">test<>'
        output = '[image 1: text][1] test'
        self.assertEqual(work_with_text.text_processing(entering, links), output)
        self.assertEqual(links, ['link'])

    def test_edit_key(self):
        entering = 'key'
        output = 'Key: '
        self.assertEqual(work_with_text.edit_key(entering), output)

        entering = 'published'
        output = 'Date: '
        self.assertEqual(work_with_text.edit_key(entering), output)

        entering = 'summary'
        output = 'Description: '
        self.assertEqual(work_with_text.edit_key(entering), output)

    def test_get_string_with_result(self):
        entering_dict = {
            'title': 'titl',
            'items': [{
                    'title': 't1',
                    'published': 'date1',
                    'link': 'link1',
                    'summary': 'des1',
                },
                {
                    'title': 't2',
                    'published': 'date2',
                    'link': 'link2',
                    'summary': 'des2'
                }
            ],
            'links': [
                'first',
                'second'
            ]
        }
        output = '\ntitl\n\nTitle: t1\nDate: date1\nLink: link1\nDescription: des1\n\n' + \
                 'Title: t2\nDate: date2\nLink: link2\nDescription: des2\n\n' + \
                 '\nLinks: \n[1] - first\n[2] - second\n'
        self.assertEqual(work_with_text.get_string_with_result(entering_dict, 2), output)


if __name__ == '__main__':
    unittest.main()
