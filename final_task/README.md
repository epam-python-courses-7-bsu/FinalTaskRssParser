# Python RSS-reader 
Python RSS-reader is a command-line utility which receives RSS URL and prints results in human-readable format.

REQUIREMENTS:
-- feedparser 5.2.1
-- fpdf 1.7.2
-- dominate 2.4.0

5 mains files of project:
* rss_reader.py - the file which runs the application
* ConsoleParse.py - contains code which parses arguments from console
* Entry.py - contains class Entry which represent an article
* Handler.py - contains class Handler which performes functions of processing objects Entry
* Logging.py - contains decorator for printing loggs in stdout
* 
To start Python RSS-reader run one of the following commands
in command line:
```shell
$ python rss_reader.py "https://news.yahoo.com/rss/" --limit 1
```
```shell
$ python rss_reader.py "https://timesofindia.indiatimes.com/rssfeedstopstories.cms" --json --limit 1
```

Structure of output when `--json` is selected:
```
{
  "Feed": "Yahoo News - Latest News & Headlines",
  "Title": "PHOTOS: #MenToo: The hidden tragedy of male sexual abuse in the military",
  "DateInt": "20200102",
  "Date": "Tue, 1 Dec 2019 ",
  "Link": "https://news.yahoo.com/photos-men-too-the-hidden-tragedy-of-male-sexual-abuse-in-the-military-005342483.html",
  "Summary": "[image 1: PHOTOS: #MenToo: The hidden tragedy of male sexual abuse in the military][1] Award-winning photojournalist Mary F. Calvert has spent six years documenting the prevalence of rape in the military and the effects on victims. She began with a focus on female victims but more recently has examined the underreported incidence of sexual assaults on men and the lifelong trauma it can inflict.",
  "Links": [
    "https://news.yahoo.com/photos-men-too-the-hidden-tragedy-of-male-sexual-abuse-in-the-military-005342483.html",
    "http://l1.yimg.com/uu/api/res/1.2/LR4Vdg0MD6osVIDtZW75aA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-12/316fa7e0-2c23-11ea-bed7-1ebe74b8c372"
  ],
  "Source": "https://news.yahoo.com/rss/"
}
```
## Iteration 2
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
$ pip install rss-reader-4.0.tar.gz
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
$ pip install rss-reader-1.0.tar.gz
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
## Iteration 3
News is stored in local file cache.json as list of json objects.
App rss-reader can accept optional argument --date
```
$ python rss_reader.py "https://news.tut.by/rss/" --date 20200102
```
```
Feed: TUT.BY: Новости ТУТ

Title: Кристин Килер, любовница британского министра и советского шпиона: кем она была на самом деле?
Date: Fri, 2 Jan 2020
Link: https://news.tut.by/culture/667279.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news

[image 2: Фото: bbc.com][2] Кристин Килер было всего 19, когда она оказалась в центре секс-скандала, приведшего к отставке британского кабинета министров. Ее выставили злодейкой, и затем всю оставшуюся жизнь эта история преследовала ее. Впервые ее трактовка событий была воплощена в сериале, созданном Би-би-си.

Links:
[0] https://news.tut.by/culture/667279.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news (link)
[1] https://img.tyt.by/n/kultura/0c/9/kristin_killer3.jpg (image)
[2] https://img.tyt.by/thumbnails/n/kultura/0c/9/kristin_killer3.jpg (image)
```
```
$ python rss_reader.py --date 20200102
```
```
Feed: Yahoo News - Latest News & Headlines

Title: PHOTOS: #MenToo: The hidden tragedy of male sexual abuse in the military
Date: Tue, 1 Dec 2019
Link: https://news.yahoo.com/photos-men-too-the-hidden-tragedy-of-male-sexual-abuse-in-the-military-005342483.html

[image 1: PHOTOS: #MenToo: The hidden tragedy of male sexual abuse in the military][1] Award-winning photojournalist Mary F. Calvert has spent six years documenting the prevalence of rape in the military and the effects on victims. She began with a focus on female victims but more recently has examined the underreported incidence of sexual assaults on men and the lifelong trauma it can inflict.

Links:
[0] https://news.yahoo.com/photos-men-too-the-hidden-tragedy-of-male-sexual-abuse-in-the-military-005342483.html (link)
[1] http://l1.yimg.com/uu/api/res/1.2/LR4Vdg0MD6osVIDtZW75aA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-12/316fa7e0-2c23-11ea-bed7-1ebe74b8c372 (image)


Feed: TUT.BY: Новости ТУТ

Title: Кристин Килер, любовница британского министра и советского шпиона: кем она была на самом деле?
Date: Fri, 2 Jan 2020
Link: https://news.tut.by/culture/667279.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news

[image 2: Фото: bbc.com][2] Кристин Килер было всего 19, когда она оказалась в центре секс-скандала, приведшего к отставке британского кабинета министров. Ее выставили злодейкой, и затем всю оставшуюся жизнь эта история преследовала ее. Впервые ее трактовка событий была воплощена в сериале, созданном Би-би-си.

Links:
[0] https://news.tut.by/culture/667279.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news (link)
[1] https://img.tyt.by/n/kultura/0c/9/kristin_killer3.jpg (image)
[2] https://img.tyt.by/thumbnails/n/kultura/0c/9/kristin_killer3.jpg (image)
```
Argument --date work with all the other arguments
```
$ python rss_reader.py --date 20191113 --json --verbose
```
## Iteration 4
Option of conversation of news in htmlf format is available. 
Example:
```
$ python rss_reader.py "https://news.yahoo.com/rss/" --to-html "F:/Path/to/your/folder" --to-pdf "F:/Path/to/your/folder"
```
Option works with all the other attributes.
```
$ python rss_reader.py --date 20191118 --to-html "F:/Path/to/your/folder" --limit 1
```
## Iteration 5
A new optional argument `--colorize` is available. It prints the news in colorized mod.
Option works with all the other attributes execept `--to-html` and `--to-pdf` arguments.
```
$ python rss_reader.py --date 20200102 --colorize
```
```diff
+ Feed: Yahoo News - Latest News & Headlines

+ Title: PHOTOS: #MenToo: The hidden tragedy of male sexual abuse in the military
+ Date: Tue, 1 Dec 2019
+ Link: https://news.yahoo.com/photos-men-too-the-hidden-tragedy-of-male-sexual-abuse-in-the-military-005342483.html

+[image 1: PHOTOS: #MenToo: The hidden tragedy of male sexual abuse in the military][1] Award-winning photojournalist Mary F. Calvert has spent six years documenting the prevalence of rape in the military and the effects on victims. She began with a focus on female victims but more recently has examined the underreported incidence of sexual assaults on men and the lifelong trauma it can inflict.

+ Links:
+ [0] https://news.yahoo.com/photos-men-too-the-hidden-tragedy-of-male-sexual-abuse-in-the-military-005342483.html (link)
+ [1] http://l1.yimg.com/uu/api/res/1.2/LR4Vdg0MD6osVIDtZW75aA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-12/316fa7e0-2c23-11ea-bed7-1ebe74b8c372 (image)
```
