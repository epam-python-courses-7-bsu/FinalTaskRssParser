# RSS Reader version 3.0 by AlexSpaceBy (fiz.zagorodnAA@gmail.com)

First, second and third iteration.

## General description:

The RssReader program takes rss url and receives news and print it in console in following form:

*========================================== RSS Reader ==============================*
*Feed: Channel feed*
*Title: Title of the news*
*Date: Day, Month year hh.mm.ss*
*Link: Link to full news*

*TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT*
*TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT*
*TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT*

*Image: Image for the news, if available.*
*(News separator). . . . . . . . . . . . . . . . .*

*Next news*

*...*

*=================================End for news=======================================*

To run the program, you should do the following:

*For Windows:*
     1. Run console as Administrator (mandatory)
     2. Type the following: `rss-reader [url] [flags] [parameters]`
*For Linux:*
     1. Type the following: `sudo rss-reader `[url] [flags] [parameters]`

Program has a number of flags described below, that can be used to control it. 
Program logs all events to `logJournal.log` file. Program writes all news to `news.log` file. 

## Program flags

Program behavior is guided by a number of flags:

`-v` - Print the version of the program in console (use: `-v`).
`-h` - Print the help message (use: `-h`).
`-b` - Print logs from logJournal to console (use: `[url] -b`).
`-j` - Print news in JSON format to console( use: `[url] -j`).
`-l` - Limit the number of news topics (use: `[url] -l [number]`).
`-d` - Date to print the news with it from history (use: `[url] -d [YYYYmmdd]`).

Since argsparse.py lib is used, it ismandatory to use positional `[url]` parameter
for `[-j]`, `[-b]`, `[-l]`, `[-d]` flags. 

## logJournal

There are three main types of events:

*1. INFO*
*2. WARNING*
*3. ERROR*

To see log journal, one needs to use `[-b]` flag. 

*For Windows:* Log Journal is stored in the default Python directory (in my case: `C:\Program Files\Python38\Lib\site-packages\rss_reader`).


*For Linux:* Log Journal is stored in the default Python directory (in my case: `/usr/local/lib/python3.7/site-packages/rss_reader`).

## Program logic description

The program has a builtin checker that checks whether the `[url]` is an actual url. 
The url must have the following format: `https://nameofthesite.domain[/rest part of the link]`.
In case `[url]` is wrong, the program tells suggests you either to change the `[ur]` or to quit.
If `[url]` looks like url, the program tryes to check if there is a server on the other side. 
If the server is not available, the program will try to reconnect to it in 10 seconds. Three
attempts will be made. In the server is not available, the program asks you either to change `[url]`
or to quit. If there is a server on the other side, the program tries to take RSS Feed. If `[url]` leads to
site, server, or something that doesn't have RSS feed, the program will ask you either to change `[url]` or to quit.
If everything is ok, the program will print news to console. The `[-l]` flag set up the limit for the news to print to console.
By default the program stores the news in local news.log file. The `[-d]` flag with `YYYYmmdd` format prints all news corresponding to
the `YYYYmmdd` date. The detailed description of news storage is described below.

## JSON format

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

## newsLog journal

By default RssReader stores all news taken from the Internet in news.log file in the following format:

*!!!#####STARTOFNEWS#####!!!YYYYmmdd*
*Feed: (line with feed)*
*Title: (line with litle)*
*Date: (line with date)*
*Link: (line with link)*
 
*TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT*
*TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT*
*TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT*

*. . . . . . . . . . . . . . . . . . .*
*!!!#####ENDOFNEWS#####!!!YYYYmmdd*

The first and the last line show the beginning and the end of news respectively. When one send `-d YYYYmmdd` command, the program searches
through all journal for the news that strat with `!!!#####STARTOFNEWS#####!!!YYYYmmdd` and ends with `!!!#####ENDOFNEWS#####!!!YYYYmmdd` and
prints all lines in between. There is a builtin function that does preliminary check of date. If date is from the future, the program will tell about it.
If there is no news.log file (that may happened if you run the program for the first time, the news.log in this case have not existed yet) or there is
no news that corresponds to the specified `YYYYmmdd` date, the program will tell about it. 

*For Windows:* News Journal is stored in the default Python directory (in my case: `C:\Program Files\Python38\Lib\site-packages\rss_reader`).

*For Linux:* News Journal is stored in the default Python directory (in my case: `/usr/local/lib/python3.7/site-packages/rss_reader`).


## General issues

Since for every RSS `[url]` can be implemented it own format, that does not fully comply with RSS specification, the program uses
html2text library to make the news text more readable. Since the program uses `argparse` standart library, there is somr difficulties with exceptions.
Namely, all Exceptions in this library inherits from Exception class, not from BaseExceptions. Because of it, all exceptions work the way they don't ment to be.

## Installation

+++++++++++++++++++++++++++++++++++++++
FOR WINDOWS (tested for Wondows 10 1903)
+++++++++++++++++++++++++++++++++++++++
Package installation:
=========================================
zip Installation:
=========================================
1. Run Console with administrator privileges (run as Administrator).
2. In console go to directory with rss-reader-3.0.zip package.
3. Run the following command: `pip install rss-reader-3.0.zip`
=========================================
zip Package Run:
=========================================
1. Run Console with administrator privileges (run as Administrator).
2. Run the following command: `rss-reader [url] [list of flags]`


+++++++++++++++++++++++++++++++++++++++
FOR LINUX (tested for Fedora 30)
+++++++++++++++++++++++++++++++++++++++
Package installation:
=========================================
zip Installation:
=========================================
1. Copy `rss-reader-3.0.zip` to desired directory (for example `~/rss-reader`).
2. In console go to directory with `rss-reader-1.0.zip` package.
3. Run the following command: `sudo pip3 install rss-reader-3.0.zip`.
=========================================
zip Package Run:
=========================================
1. In console run the following command: `sudo rss-reader [url] [list of flags]`


+++++++++++++++++++++++++++++++++++++++
CREATION OF PACKAGE
++++++++++++++++++++++++++++++++++++++
How to create package using setup.py
======================================
1. Download RssReader to desired directory
2. Go to the `.../rss-reader` folder wich has setup.py file
3.1 Windows: Run console as administrator
   3.1.1 Run the following code: `python setup.py sdist --formats=zip`
3.1 Linux: Run the following command: `sudo python3 sdist --formats=zip`
4. The zip package will be inside `.../rss-reader/dist` folder.


## progect structure

RssReader
|---rss-reader
|    |
|    |---args_parser.py
|    |---json_converter.py
|    |---logs.py
|    |---other.py
|    |---news.py
|    |---rss_reader.py
|    |---rss_parser.py
|    |---requirements.txt
|    |---tests
|        |-----test_args_parser.py
|        |-----test_rss_parser.py
|
|---setup.py
|---README.txt
|---__init__.py


## Resourses for testing

RssReader was tested with following RSS:

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


   
 