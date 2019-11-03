# RSS Reader version 1.0 by git user AlexSpaceBy (fiz.zagorodnAA@gmail.com)

 First and second iteration

## Brief description

The package for installation (second iteration) is stored inside .../RssReader/dist (RssReader-1.0.zip).
The RssReader program takes rss url and receives news and print it in console in following form:

*========================================== RSS Reader ==============================*
*Feed: Channel feed*
*Title: Title of the news*
*Date: Day, Month year hh.mm.ss*
*Link: Link to full news*

*************************TEXT WITH NEWS*****************************************
*************************TEXT WITH NEWS*****************************************
*************************TEXT WITH NEWS*****************************************
*************************TEXT WITH NEWS*****************************************

*Image: Image for the news, if available.*
*(News separator). . . . . . . . . . . . . . . . .*

*Next news*

...

*=================================End for news===================================*

## Description of the program

Program has a number of flags described below, that can be used to control it. 
Program logs all events to logJournal.log file. There are three main types of events:

1. INFO
2. WARNING
3. ERROR

To see log journal, one needs to use `[-b]` flag. Since argsparse.py lib is used, it is
mandatory to use positional `[url]` parameter for `[-j]`, `[-b]`, `[-l]` flags. For log journal one
can use any number of symbols for `[ur]` (just type: `url -b`).

The program has a builtin checker that checks whether the `[url]` is an actual url. 
The url must have the following format: *https://nameofthesite.domain[/rest part of the link]*.
In case `[url]` is wrong, the program tells suggests you either to change the `[ur]` or to quit.
If [url] looks like url, the program tryes to check if there is a server on the other side. 
If the server is not available, the program will try to reconnect to it in 10 seconds. Three
attempts will be made. In the server is not available, the program asks you either to change `[url]`
or to quit. If there is a server on the other side, the program tries to take RSS Feed. If `[url]` leads to
site, server, or something that doesn't have RSS feed, the program will ask you either to change `[url]` or to quit.
If everything is ok, the program will print news to console. The `[-l]` flag set up the limit for the news to print to console.

## JSON format description

There is a builtin JSON converter that converts the output to the specified format. The converter envokes by using `[-j]` flag.
It prints the news in JSON format to console (by using json library). The program uses the folloving JSON formatting:

{
"feed": string,
"link": string,
"title": string,
"date": datetime,
"description": string,
"image": string
}

The whole feed can be stored in JSON format by using the following formatting:

{
int: {
       "feed": string,
        "link": string,
        "title": string,
        "date": datetime,
        "description": string,
        "image": string
     },
int: {
       "feed": string,
        "link": string,
        "title": string,
        "date": datetime,
        "description": string,
        "image": string
     },
...
int: {
       "feed": string,
        "link": string,
        "title": string,
        "date": datetime,
        "description": string,
        "image": string
     }
}

Maximum int corresponds either to `[-l]` flag, or to the whole number of news for the server (for some it can be 50, for some it can be 100). 

Since for every RSS `[url]` can be implemented it own format, that does not fully comply with RSS specification, the program uses
html2text library to make the news text more readable. This library (actually it is a package) is included in the RssReader
and already configured for use. 

# How to install and run


## FOR WINDOWS (tested for Wondows 10 1903)

**Package installation:**
=========================================
**zip Installation:**
=========================================
1. Run Console with administrator privileges (run as Administrator).
2. In console go to directory with RssReader-1.0.zip package.
3. Run the following command: `pip install RssReader-1.0.zip`.
=========================================
**zip Package Run:**
=========================================
1. Run Console with administrator privileges (run as Administrator).
2. Run the following command: `RssReader.exe [url] [list of flags]`

Warning:
1. `[url]` is a positional argument, it is mandatory to enter this argument, if you use `[-b]`, `[-j]`, `[-l]` flags. For `[-b]` flag use any `[url]` you want.
2. Running console as administrator during the session is a mandatory since log is being written to the protected (by default) directory.

========================================
**Log Journal:**
========================================
**Log Journal is stored in the default Python directory (in my case: C:\Program Files\Python38\Lib\site-packages\RssReader).**
========================================


## FOR LINUX (tested for Fedora 30)

**Package installation:**
=========================================
**zip Installation:**
=========================================
1. Copy RssReader-1.0.zip to desired directory (for example ~/RssReader).
2. In console go to directory with RssReader-1.0.zip package.
3. Run the following command: `sudo pip3 install RssReader-1.0.zip`.
=========================================
**zip Package Run:**
=========================================
1. In console run the following command: `sudo RssReader [url] [list of flags]`.

Warning:
1. `[url]` is a positional argument, it is mandatory to enter this argument, if you use `[-b]`, `[-j]`, `[-l]` flags. For `[-b]` flag use any `[url]` you want.
2. Running console using `sudo` during the session is a mandatory since log is being written to the protected (by default) directory.

========================================
**Log Journal:**
========================================
**Log Journal is stored in the default Python directory (in my case: /usr/local/lib/python3.7/site-packages/RssReader).**
========================================


## DIRECT USE OF *.PY FILES

**Direct package run**
=======================================
1. Download RssReader folder to desired directory
2. Go to the `...\RssReader` folder wich has `__main__.py` file
**3.1 Windows:** Run console as administrator
   3.1.1 Run the following code: `python __main__.py [url] [flags]`
   3.1.2 Log Journal is stored in the default Python directory (in my case: C:\Program Files\Python38\Lib\site-packages\RssReader).
**3.1 Linux:** Run the following command: `sudo python3 __main__.py [url] [flags]`
    3.1.1 Log Journal is stored in the default Python directory (in my case: /usr/local/lib/python3.7/site-packages/RssReader).

Warning:
1. `[url]` is a positional argument, it is mandatory to enter this argument, if you use `[-b]`, `[-j]`, `[-l]` flags. For `[-b]` flag use any `[url]` you want.
2. Running console using "sudo" during the session is a mandatory since log is being written to the protected (by default) directory.


## CREATION OF PACKAGE

**How to create package using setup.py**
======================================
1. Download RssReader to desired directory
2. Go to the `...\RssReader` folder wich has `setup.py` file
**3.1 Windows:** Run console as administrator
   3.1.1 Run the following code: `python setup.py sdist --formats=zip`
**3.1 Linux:** Run the following command: `sudo python3 sdist --formats=zip`
4. The zip package will be inside `.../RssReader/dist` folder.


## FLAGS

**List of flags**
=======================================

-v - Print the version of the program in console.
-h - Print the help message.
-b - Print logs from logJournal to console.
-j - Print news in JSON format to console.
-l - Limit the number of news topics.
=======================================


## STRUCTURE OF THE PROJECT


RssReader
|---RssReader
|    |__init__.py
|    |__main__.py
|    |---args_parser.py
|    |---ecxeptions.py
|    |---feedparser.py
|    |---json_converter.py
|    |---logs.py
|    |---other.py
|    |---rss_reader.py
|    |---rss_parser.py
|    |
|    |---html2text
|        |-----__init__.py
|        |-----__main__.py
|        |-----cli.py
|        |-----config.py
|        |-----utils.py
|
|---setup.py
|---README.txt
|---LICENCE.txt
|---dist
    |-----RssReader-1.0.zip



## RssReader TEST

**RssReader was tested with following RSS:**
========================================

http://feeds.bbci.co.uk/news/rss.xml?edition=int
https://news.yahoo.com/rss/
https://3dnews.ru/news/rss/
https://www.tomshardware.com/feeds/all
https://people.onliner.by/feed
http://static.feed.rbc.ru/rbc/logical/footer/news.rss
https://www.gazeta.ru/export/rss/first.xml
https://rss.nytimes.com/services/xml/rss/nyt/World.xml
https://www.reddit.com/r/worldnews/.rss
https://www.aljazeera.com/xml/rss/all.xml
http://feeds.washingtonpost.com/rss/world
https://www.engadget.com/rss.xml


   
 