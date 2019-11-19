import os
import sys
import unittest
out_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(out_dir)
from Entry import Entry


class TestEntry(unittest.TestCase):
    def test__init__(self):
        entry = Entry()
        self.assertIsInstance(entry, Entry)
        self.assertNotIsInstance("entry", Entry)

    def test_parse_html(self):
        entry = Entry()
        self.assertEqual(entry.parse_html
                         (
                          "Graham now says Trump&#39;s Ukraine policy was too &#39;incoherent&#39; for quid pro quo"
                          ), "Graham now says Trump's Ukraine policy was too 'incoherent' for quid pro quo"
                         )
        self.assertEqual(entry.parse_html(
            '<p><a href="https://news.yahoo.com/graham-trump-ukraine-incoherent-quid-pro-quo-192210175.html">'
            '<img src="http://l2.yimg.com/uu/api/res/1.2/aWhGys7_IW5qIjKaiJpPfg--/YXBwaWQ9eXRhY2h5b247aD04Njt'
            '3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/5527ffe0-00'
            'ca-11ea-9f7d-d1e736c1315d" width="130" height="86" alt="Graham now says Trump&#39;s Ukraine poli'
            'cy was too &#39;incoherent&#39; for quid pro quo" align="left" title="Graham now says Trump&#39;'
            's Ukraine policy was too &#39;incoherent&#39; for quid pro quo" border="0" ></a>A day after sayi'
            'ng he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and hi'
            's conclusion is that the Trump administration’s Ukraine policy was too &quot;incoherent&quot; fo'
            'r it to have orchestrated the quid pro quo at the heart of the impeachment inquiry.<p><br clear="all">'
            ),
            "[image 0: Graham now says Trump's Ukraine policy was too 'incoherent' for quid pro quo][0] A day after "
            "saying he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and his "
            "conclusion is that the Trump administration’s Ukraine policy was too \"incoherent\" for it to have"
            " orchestrated the quid pro quo at the heart of the impeachment inquiry."
        )
        self.assertNotEqual(entry.parse_html
            (
            "Graham now says Trump&#39;s Ukraine policy was too &#39;incoherent&#39; for quid pro quo"
        ),
            "Ukraine policy was too 'incoherent' for quid pro quo"
        )
        self.assertNotEqual(entry.parse_html(
            '<p><a href="https://news.yahoo.com/graham-trump-ukraine-incoherent-quid-pro-quo-192210175.html">'
            '<img src="http://l2.yimg.com/uu/api/res/1.2/aWhGys7_IW5qIjKaiJpPfg--/YXBwaWQ9eXRhY2h5b247aD04Njt'
            '3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/5527ffe0-00'
            'ca-11ea-9f7d-d1e736c1315d" width="130" height="86" alt="Graham now says Trump&#39;s Ukraine poli'
            'cy was too &#39;incoherent&#39; for quid pro quo" align="left" title="Graham now says Trump&#39;'
            's Ukraine policy was too &#39;incoherent&#39; for quid pro quo" border="0" ></a>A day after sayi'
            'ng he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and hi'
            's conclusion is that the Trump administration’s Ukraine policy was too &quot;incoherent&quot; fo'
            'r it to have orchestrated the quid pro quo at the heart of the impeachment inquiry.<p><br clear="all">'
        ),
            "[image 5: Graham now says Trump's Ukraine policy was too 'incoherent' for quid pro quo][5] A day after "
            "saying he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and his "
            "conclusion is that the Trump administration’s Ukraine policy was too \"incoherent\" for it to have"
            " orchestrated the quid pro quo at the heart of the impeachment inquiry."
        )


if __name__ == '__main__':
    unittest.main()
