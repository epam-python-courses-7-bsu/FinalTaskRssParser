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
    "Title": "Is Nikki Haley auditioning to replace Pence on Trump's 2020 ticket?",
    "DateInt": "20191112",
    "Date": "Tue, 12 Nov 2019 11:34:28 -0500",
    "Link": "https://news.yahoo.com/nikki-haley-book-tour-audition-vp-pence-trump-2020-ticket-163428688.html",
    "Summary": "[image 1: Is Nikki Haley auditioning to replace Pence on Trump's 2020 ticket?][1] Less than three months ago, the former U.S. ambassador to the United Nations tried to tamp down speculation that she might replace the vice president on Trump\u2019s 2020 ticket. But multiple political observers say her new book tour is doubling as an audition for the role.",
    "Links": [
      "https://news.yahoo.com/nikki-haley-book-tour-audition-vp-pence-trump-2020-ticket-163428688.html",
      "http://l2.yimg.com/uu/api/res/1.2/XnMA9mstMRV0FkOdMugjhg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/f1884750-fcd3-11e9-bcf7-cef09bc7ad91"
    ]
  }
```
# Iteration 2
If you have installed Python then to export CLI utility rss-reader follow these steps:
1. Clone this repository
```
$ git clone https://github.com/IlyaTorch/FinalTaskRssParser.git
```
2. Go to the directory FinalTaskRssParser\final_task
3. run ```$ python setup.py sdist```
4. Go to the directory dist
```
$ cd dist
```
5. Install CLI utility rss-reader:
```
$pip install rss-reader-1.0.tar.gz
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
If you don't have installed Python, follow these steps:
1. Download and install python from https://www.python.org/downloads/
2. Clone this repository
```
$ git clone https://github.com/IlyaTorch/FinalTaskRssParser.git
```
2. Go to the directory FinalTaskRssParser\final_task
3. run ```$ python setup.py sdist```
4. Go to the directory dist
```
$ cd dist
```
5. Install CLI utility rss-reader:
```
$pip install rss-reader-1.0.tar.gz
```
And we can use it:
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
# Iteration 3
rss-reader can accept optional argument --date instead of argument source
```
$ python rss_reader.py --date 20191113
```
```
$ python rss_reader.py "https://news.yahoo.com/rss/"  --date 20191113
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     [--date DATE]
                     [source]
rss_reader.py: error: argument --date: not allowed with argument source
```
Argument --date work with --json, --limit and --verbose arguments
```
$ python rss_reader.py --date 20191113 --json --verbose
```
News is stored in local file cache.json as list of json objects
# Iteration 4
Option of conversation of news in htmlf format is available. 
REQUIREMENTS:
-- feedparser 5.2.1
-- fpdf 1.7.2
Example:
```
$ python rss_reader.py "https://news.yahoo.com/rss/" --to-html "F:/Path/to/your/folder" --to-pdf "F:/Path/to/your/folder"
```
Option works with --limit and --date attributes
```
$ python rss_reader.py --date 20191118 --to-html "F:/Path/to/your/folder" --limit 1
```
Option throws an exception when the path to the folder is incorrect
```
$ python rss_reader.py "https://news.yahoo.com/rss/" --to-html "F:/incorrect/path"
Error. No such folder. Check the correctness of the entered path
```
When you try to output the news to the opened file:
```
Error, close the file for output of news
```
