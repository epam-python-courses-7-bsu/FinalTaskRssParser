import unittest
from final_task.rss_reader.parse_rss_functions import get_new_description, get_image_description
class TestMethods(unittest.TestCase):
    def test_get_new_description(self):
        summary_str='<p><a href="https://news.yahoo.com/alexandria-ocasio-cortez-says-impeachment-inquiry-is-at-' \
                    'the-point-of-no-return-182636649.html"><img src="http://l2.yimg.com/uu/api/res/1.2/btX_' \
                    'WaWRmBpwx4hlgfiNIw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.' \
                    'amazonaws.com/creatr-uploaded-images/2019-11/77d7ab00-0ae6-11ea-9aff-813c7f464d0a" width="130"' \
                    ' height="86" alt="Ocasio-Cortez: Trump was &#39;clearly engaged in extortion and bribery\';" ' \
                    'align="left" title="Ocasio-Cortez: Trump was \';clearly engaged in extortion and ' \
                    'bribery\';" border="0" ></a>Ocasio-Cortez discussed the issue with Yahoo News on ' \
                    'Capitol Hill on Tuesday as the third day of public hearings was being conducted in ' \
                    'the Democrats’ ongoing impeachment inquiry.<p><br clear="all">'
        correct_result='Ocasio-Cortez discussed the issue with Yahoo News on Capitol Hill on Tuesday as ' \
                       'the third day of public hearings was being conducted in the Democrats’ ' \
                       'ongoing impeachment inquiry.'
        self.assertEqual(get_new_description(summary_str),correct_result)

    def test_get_image_description(self):
        summary_str = '<p><a href="https://news.yahoo.com/alexandria-ocasio-cortez-says-impeachment-inquiry-is-at-' \
                      'the-point-of-no-return-182636649.html"><img src="http://l2.yimg.com/uu/api/res/1.2/btX_' \
                      'WaWRmBpwx4hlgfiNIw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.' \
                      'amazonaws.com/creatr-uploaded-images/2019-11/77d7ab00-0ae6-11ea-9aff-813c7f464d0a" width="130"' \
                      ' height="86" alt="Ocasio-Cortez: Trump was &#39;clearly engaged in extortion and bribery\';" ' \
                      'align="left" title="Ocasio-Cortez: Trump was \';clearly engaged in extortion and ' \
                      'bribery\';" border="0" ></a>Ocasio-Cortez discussed the issue with Yahoo News on ' \
                      'Capitol Hill on Tuesday as the third day of public hearings was being conducted in ' \
                      'the Democrats’ ongoing impeachment inquiry.<p><br clear="all">'
        correct_result="Ocasio-Cortez: Trump was &#39;clearly engaged in extortion and bribery';"
        self.assertEqual(get_image_description(summary_str), correct_result)


if __name__ == '__main__':
    unittest.main()