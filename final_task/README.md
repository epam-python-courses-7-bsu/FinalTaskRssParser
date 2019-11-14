# RSS Reader version 3.5 by AlexSpaceBy (fiz.zagorodnAA@gmail.com)

First, second, third and half of fourth iteration.

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
`-p` - Convert news to pdf and store it locally (use: `[url] -p [destination folder]`).

Since argsparse.py lib is used, it ismandatory to use positional `[url]` parameter
for `[-j]`, `[-b]`, `[-l]`, `[-d]`, `[-p]` flags. 

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
the `YYYYmmdd` date. The detailed description of news storage is described below. There is an option to convert nwes to pdf. The detailed
description of this option is provided below.

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
*Image: (line with image)*
 
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
There is a builtin function that checks whether the news has been already added to the local storage. If so, the program logs the attempt, and does not add it to
the local storage. To use this function the program takes the link for the news and checks if there is a news with the same link.

Typical usage (provided you have the news log in your local storage, if not, just provide a valid rss url to create one):

               `rss-reader url -d 20191113` - prints all news for 2019.11.13 to console from local storage

               `rss-reader url -d 20191113 -l 10` - prints 10 news for 2019.11.13 to console from local storage

*For Windows:* News Journal is stored in the default Python directory (in my case: `C:\Program Files\Python38\Lib\site-packages\rss_reader`).

*For Linux:* News Journal is stored in the default Python directory (in my case: `/usr/local/lib/python3.7/site-packages/rss_reader`).

## Convert news to pdf

The program can convert the news to pdf. It can take either news from the Internet, or from local storage. The program converts news to pdf by invoking `[-p]` flag.
In the document the program provide all data about the news, including image and link. If the image is not available, or corrupted, the program will let you know about it.
The image and link are interactive and can be used as URL for the sourse by clicking.

Typical usage of the pdf converter (if it was installed from the package):

                                  `rss-reader https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\` - convert all news from the feed to pdf. 

                                  `rss-reader https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\ -l 10` - convert 10 news from the feed to pdf.

                                  `rss-reader https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\ -l 10 -j` - convert 10 news from the json feed to pdf.

                                  `rss-reader url -b -p C:\Users\User\Destination_Folder\` - convert log journal to pdf

                                  `rss-reader url -d 20191113 -p C:\Users\User\Destination_Folder\` - convert all news from the local storage to pdf for 20191113.

                                  `rss-reader url -d 20191113 -p C:\Users\User\Destination_Folder\ -l 10` - convert 10 news from the local storage to pdf for 20191113.



The `Destination_Folder\` is a folder where files after pdf conversion will be stored. The `\` in the end of the path is a mandatory for the program. If the `Destination_Folder` does not exist, or you have no permission to create pdf inside it,
the program will let you know. Since pdf convertion is a heavy weight procedure, it can take time. If ther is no errors, just wait until it converts.  

## General issues

Since for every RSS `[url]` can be implemented it own format, that does not fully comply with RSS specification, the program uses
html2text library to make the news text more readable. Since the program uses `argparse` standart library, there is somr difficulties with exceptions.
Namely, all Exceptions in this library inherits from Exception class, not from BaseExceptions. Because of it, all exceptions work the way they don't ment to be.

## Installation

+++++++++++++++++++++++++++++++++++++++
CREATION OF PACKAGE
++++++++++++++++++++++++++++++++++++++
How to create package using setup.py
======================================
1. Go to the */final_task* folder wich has `setup.py` file

3.1 Windows: Run console as Administrator
   3.1.1 Run the following code: `python setup.py sdist --formats=zip`

3.1 Linux: Run the following command: `sudo python3 setup.py sdist --formats=zip` (provided your python v3.8 has a shortcut `python3`)

4. The zip package will be inside `.../final_task/dist` folder.

+++++++++++++++++++++++++++++++++++++++
INSTALLATION FOR WINDOWS (tested for Wondows 10 1903)
+++++++++++++++++++++++++++++++++++++++
Package installation:
=========================================
zip Installation:
=========================================
1. Run Console with administrator privileges (run as Administrator).
2. In console go to directory with *rss-reader-3.5.zip* package.
3. Run the following command: `pip install rss-reader-3.5.zip`
=========================================


+++++++++++++++++++++++++++++++++++++++
INSTALLATION FOR LINUX (tested for Fedora 30)
+++++++++++++++++++++++++++++++++++++++
Package installation:
=========================================
zip Installation:
=========================================
1. In console go to directory with *rss-reader-3.5.zip* package.
2. Run the following command: `sudo pip3 install rss-reader-3.5.zip`.
=========================================



## How to run the program

DIRECT RUN FROM rss_reader FOLDER:
====================================================================================================================
WARINING:
If you try to run directly from the folder, and have never installed the program from the package, YOU MUST INSTALL the following packages:

Windows:
1. feedparser version 5.2.1 (`pip install feedparser==5.2.1`)
2. html2text version 2019.9.26 (`pip install html2text==2019.9.26`)
3. fpdf version 1.7.2 (`pip install fpdf==1.7.2`)

Linux:
1. feedparser version 5.2.1 (`sudo pip3 install feedparser==5.2.1`)
2. html2text version 2019.9.26 (`sudo pip3 install html2text==2019.9.26`)
3. fpdf version 1.7.2 (`sudo pip3 install fpdf==1.7.2`)
====================================================================================================================

Windows:
========
1. Run console as Administrator.
2. Go to */rss_reader* folder with `rss_reader.py` file.
3. Run: `python rss_reader.py [flags] [parameters]` 

Example:
 `python rss_reader.py https://news.yahoo.com/rss/` - will show you RSS feed from mews.yahoo
 `python rss_reader.py https://news.yahoo.com/rss/ -l 10` - will show you RSS feed with 10 news
 `python rss_reader.py https://news.yahoo.com/rss/ -v` - will show you version of the program
 `python rss_reader.py https://news.yahoo.com/rss/ -l 10 -j` - will show you RSS feed with 10 news in JSON format

 `python rss_reader.py url -b` - will show you log journal

 `python rss_reader.py url -d 20191113` - prints all news for 2019.11.13 to console from local storage
 `python rss_reader.py url -d 20191113 -l 10` - prints 10 news for 2019.11.13 to console from local storage

 `python rss_reader.py https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\` - convert all news from the feed to pdf. 
 `python rss_reader.py https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\ -l 10` - convert 10 news from the feed to pdf.
 `python rss_reader.py https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\ -l 10 -j` - convert 10 news from the json feed to pdf.
 `python rss_reader.py url -b -p C:\Users\User\Destination_Folder\` - convert log journal to pdf
 `python rss_reader.py url -d 20191113 -p C:\Users\User\Destination_Folder\` - convert all news from the local storage to pdf for 20191113.
 `python rss_reader.py url -d 20191113 -p C:\Users\User\Destination_Folder\ -l 10` - convert 10 news from the local storage to pdf for 20191113.

Linux:
======
1. Open the console
2. Go to */rss_reader* folder with `rss_reader.py` file.
3. Run: `sudo python3 rss_reader.py [flags] [parameters]` (provided your python v3.8 has a shortcut `python3`)

Example:
 `sudo python3 rss_reader.py https://news.yahoo.com/rss/` - will show you RSS feed from mews.yahoo
 `sudo python3 rss_reader.py https://news.yahoo.com/rss/ -l 10` - will show you RSS feed with 10 news
 `sudo python3 rss_reader.py https://news.yahoo.com/rss/ -v` - will show you version of the program
 `sudo python3 rss_reader.py https://news.yahoo.com/rss/ -l 10 -j` - will show you RSS feed with 10 news in JSON format

 `sudo python3 rss_reader.py url -d 20191113` - prints all news for 2019.11.13 to console from local storage
 `sudo python3 rss_reader.py url -d 20191113 -l 10` - prints 10 news for 2019.11.13 to console from local storage

 `sudo python3 rss_reader.py https://news.yahoo.com/rss/ -p /Users/User/Destination_Folder/` - convert all news from the feed to pdf. 
 `sudo python3 rss_reader.py https://news.yahoo.com/rss/ -p /Users/User/Destination_Folder/ -l 10` - convert 10 news from the feed to pdf.
 `sudo python3 rss_reader.py https://news.yahoo.com/rss/ -p /Users/User/Destination_Folder/ -l 10 -j` - convert 10 news from the json feed to pdf.
 `sudo python3 rss_reader.py url -b -p /Users/User/Destination_Folder/` - convert log journal to pdf
 `sudo python3 rss_reader.py url -d 20191113 -p /Users/User/Destination_Folder/` - convert all news from the local storage to pdf for 20191113.
 `sudo python3 rss_reader.py url -d 20191113 -p /Users/User/Destination_Folder/ -l 10` - convert 10 news from the local storage to pdf for 20191113.

All files like logJournal and news.log will be inside rss_reader directory.
=====================================================================================================================


PACKAGE RUN (assume you did every step from Installation and installed rss-reader-3.1.zip)
=====================================================================================================================
Windows:
========
1. Run console as Administrator.
3. Run: `rss-reader [flags] [parameters]` 

Example:
 `rss-reader https://news.yahoo.com/rss/` - will show you RSS feed from mews.yahoo
 `rss-reader https://news.yahoo.com/rss/ -l 10` - will show you RSS feed with 10 news
 `rss-reader https://news.yahoo.com/rss/ -v` - will show you version of the program
 `rss-reader https://news.yahoo.com/rss/ -l 10 -j` - will show you RSS feed with 10 news in JSON format

 `rss-reader url -b` - will show you log journal

 `rss-reader url -d 20191113` - prints all news for 2019.11.13 to console from local storage
 `rss-reader url -d 20191113 -l 10` - prints 10 news for 2019.11.13 to console from local storage

 `rss-reader https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\` - convert all news from the feed to pdf. 
 `rss-reader https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\ -l 10` - convert 10 news from the feed to pdf.
 `rss-reader https://news.yahoo.com/rss/ -p C:\Users\User\Destination_Folder\ -l 10 -j` - convert 10 news from the json feed to pdf.
 `rss-reader url -b -p C:\Users\User\Destination_Folder\` - convert log journal to pdf
 `rss-reader url -d 20191113 -p C:\Users\User\Destination_Folder\` - convert all news from the local storage to pdf for 20191113.
 `rss-reader url -d 20191113 -p C:\Users\User\Destination_Folder\ -l 10` - convert 10 news from the local storage to pdf for 20191113.

All files like logJournal and news.log will be inside the default Python directory (in my case: `C:\Program Files\Python38\Lib\site-packages\rss_reader`).

Linux:
======
1. Run the console.
3. Run: `sudo rss-reader [flags] [parameters]` (provided your python v3.8 has a shortcut `python3`)

Example:
 `sudo rss-reader https://news.yahoo.com/rss/` - will show you RSS feed from mews.yahoo
 `sudo rss-reader https://news.yahoo.com/rss/ -l 10` - will show you RSS feed with 10 news
 `sudo rss-reader https://news.yahoo.com/rss/ -v` - will show you version of the program
 `sudo rss-reader https://news.yahoo.com/rss/ -l 10 -j` - will show you RSS feed with 10 news in JSON format

 `sudo rss-reader url -b` - will show you log journal

 `sudo rss-reader url -d 20191113` - prints all news for 2019.11.13 to console from local storage
 `sudo rss-reader url -d 20191113 -l 10` - prints 10 news for 2019.11.13 to console from local storage

 `sudo rss-reader https://news.yahoo.com/rss/ -p /Users/User/Destination_Folder/` - convert all news from the feed to pdf. 
 `sudo rss-reader https://news.yahoo.com/rss/ -p /Users/User/Destination_Folder/ -l 10` - convert 10 news from the feed to pdf.
 `sudo rss-reader https://news.yahoo.com/rss/ -p /Users/User/Destination_Folder/ -l 10 -j` - convert 10 news from the json feed to pdf.
 `sudo rss-reader url -b -p /Users/User/Destination_Folder/` - convert log journal to pdf
 `sudo rss-reader url -d 20191113 -p /Users/User/Destination_Folder/` - convert all news from the local storage to pdf for 20191113.
 `sudo rss-reader url -d 20191113 -p /Users/User/Destination_Folder/ -l 10` - convert 10 news from the local storage to pdf for 20191113.

All files like logJournal and news.log will be inside the default Python directory (in my case: `/usr/local/lib/python3.7/site-packages/rss_reader`).

## progect structure

final_task
|---rss-reader
|    |
|    |---args_parser.py
|    |---json_converter.py
|    |---logs.py
|    |---other.py
|    |---news.py
|    |---rss_reader.py
|    |---rss_parser.py
|    |---converter.py
|    |---ARIALUNI.TTF
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

https://news.yahoo.com/rss/
https://3dnews.ru/news/rss/
https://www.tomshardware.com/feeds/all
https://people.onliner.by/feed
http://feeds.bbci.co.uk/news/rss.xml?edition=int
http://static.feed.rbc.ru/rbc/logical/footer/news.rss
https://www.gazeta.ru/export/rss/first.xml
https://rss.nytimes.com/services/xml/rss/nyt/World.xml
https://www.reddit.com/r/worldnews/.rss
https://www.aljazeera.com/xml/rss/all.xml
http://feeds.washingtonpost.com/rss/world
https://www.engadget.com/rss.xml


   
 