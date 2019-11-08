# Python RSS-reader 
Python RSS-reader is a command-line utility which receives RSS URL and prints results in human-readable format.

To start Python RSS-reader run one of the following commands
in command line:
```shell
python rss_reader.py "https://news.yahoo.com/rss/" --limit 1
```
```shell
python rss_reader.py "https://timesofindia.indiatimes.com/rssfeedstopstories.cms" --json --limit 1
```
```shell
python rss_reader.py "http://www.nato.int/cps/rss/en/natohq/rssFeed.xsl/rssFeed.xml" --limit 1
```

5 mains files of project:
* rss_reader.py - the file which runs the application
* ConsoleParse.py - contains code which parses arguments from console
* Entry.py - contains class Entry which represent an article
* Handler.py - contains class Handler which performes functions of processing objects Entry
* Logging.py - contains decorator for printing loggs in stdout

Structure of output when `--json` is selected:
```
{
  "Feed": "Yahoo News - Latest News & Headlines",
  "Title": "Trump Jr. tweets name of alleged whistleblower",
  "Date": "Wed, 06 Nov 2019 11:44:34 -0500",
  "Link": "https://news.yahoo.com/donald-trump-jr-tweets-name-of-whistleblower-164434463.html",
  "Links": [
    "https://news.yahoo.com/donald-trump-jr-tweets-name-of-whistleblower-164434463.html",
    "http://l.yimg.com/uu/api/res/1.2/2BQtOMLnlPTy3DNXkpQPIw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/e7ce4300-00b0-11ea-abff-085279fefba1"
  ]
}
```
# Iteration 2
To export CLI utility rss-reader follow these steps:
```
cd dist
pip install rss-reader-1.0.tar.gz
```
And we can use CLI utility rss-reader:
```
rss-reader "https://news.yahoo.com/rss/" --limit 1
```
```
Feed:  Yahoo News - Latest News & Headlines

Title:  Graham now says Trump's Ukraine policy was too 'incoherent' for quid pro quo
Date:  Wed, 06 Nov 2019 14:22:10 -0500
Link:  https://news.yahoo.com/graham-trump-ukraine-incoherent-quid-pro-quo-192210175.html


[image 1: Graham now says Trump's Ukraine policy was too 'incoherent' for quid pro quo][1] A day after saying he wouldn’t bother to read the testimony, Sen. Lindsey Graham now says he did read it, and his conclusion is that the Trump administration’s Ukraine policy was too "incoherent" for it to have orchestrated the quid pro quo at the heart of the impeachment inquiry.


Links:
[0]  https://news.yahoo.com/graham-trump-ukraine-incoherent-quid-pro-quo-192210175.html (link)
[1]  http://l2.yimg.com/uu/api/res/1.2/aWhGys7_IW5qIjKaiJpPfg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/5527ffe0-00ca-11ea-9f7d-d1e736c1315d (image)
```