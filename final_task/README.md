# Python RSS-reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

**Utility provides the following interface:**

```
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     [--date DATE] [--to-html TO_HTML] [--to-pdf TO_PDF]
                     [--colorize]
                     [source]

Performs a variety of operations on a file.

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limits the number of displayed news
  --date DATE        Displays news for the specified day. It takes a date in %Y%m%d format.
  --to-html TO_HTML  Converts news in html format. Receives the path for file
                     saving
  --to-pdf TO_PDF    Converts news in pdf format. Receives the path for file
                     saving
  --colorize         Make stdout in colour
```

In addition to the --verbose argument, the utility also provides recording logging events in a event_tracker.log file that remembering all messages from earlier runs.



## Requirements

The REST API was created using Python 3.8. To run the APP you need to install with pip packages listed in [requirements.txt](https://github.com/brechka/FinalTaskRssParser/blob/master/final_task/rss_reader/requirements.txt) 
(better to use virtual environment):

```
pip install -r requirements.txt
```



## Usage of RSS-reader

The entire application is contained within the rss_reader.py file. For running the utility use previously listed command line arguments. For example:

```
rss_reader.py https://news.yahoo.com/rss/ --limit 1
```

The output will be the following structure:

```
Feed: Yahoo News - Latest News & Headlines

Title: GOP claim that Trump cares about corruption takes a hit at impeachment hearing

Date: Wed, 20 Nov 2019 20:26:09 -0500
Link: https://news.yahoo.com/gop-claim-that-trump-cares-about-corruption-takes-a-hit-at-impeachment-heaing-012609516.html

[image 2: GOP claim that Trump cares about corruption takes a hit at impeachment hearing]
Rep. Jim Himes, D-Conn., took issue with a defense of President Trump floated by Rep. John Ratcliffe, R-Texas.

Links:
[1]: https://news.yahoo.com/gop-claim-that-trump-cares-about-corruption-takes-a-hit-at-impeachment-heaing-012609516.html (link to the article)

[2]: http://l.yimg.com/uu/api/res/1.2/cpj4jzp35ZTzQ6ds8B1M0w--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/64948b40-0bee-11ea-ad7c-1300326b62d1
```



## Description

###### [rss_reader/rss_reader.py](https://github.com/brechka/FinalTaskRssParser/blob/master/final_task/rss_reader/rss_reader.py)

In rss_reader.py RSS-reader utility is initialized and configured. The utility provides the following features:

##### 1) *Data caching:*

The RSS news are stored in the local storage while reading. For this purpose [shelve](https://docs.python.org/3/library/shelve.html), dictionary-like object, was used.
With the optional argument ```--date %Y%m%d``` (for example: ```--date 20191120```) the cashed news can be read. Also, adding URL make the displayed news sorted by date and link. 
If the news are not found - error should be returned.

##### 2) *Data conversion to .pdf and .html:*

The RSS-reader utility provides news converter to .pdf and .html formats. It can be accomplished with the following optional arguments: ```--to-pdf``` and ```--to-html```.
Both arguments receive the path where new file would be saved. The name of the file generates automatically.
There are two options for news conversion:

- *convert from cache*

For this case news conversion doesn't depend on internet. With ```rss_reader.py --date 20191120 --limit 1 --to-html ~/finaltask/rss-reader``` one news for the specified day would be converted (the same with ```--to-pdf```), and file with it would be generated in the specified PATH.
There would be clickable links to the full article and images.

- *convert fresh news from the Internet*

For this case Internet is required. With ```rss_reader.py https://news.yahoo.com/rss/ --limit 1 --to-html ~/finaltask/rss-reader``` one news from listed link would be converted (the same with ```--to-pdf```), and file with it would be generated in the specified PATH.
In this case all pictures would be clickable and would be displayed, if the format permits. Otherwise, there would be clickable links to the images. Also result would be contain a links to the full articles.

##### 3) *Output in colour:*

For colorizing the output there are ```--colorize``` optional argument. Utility provides colorization of the logs and RSS news output (json included).