# Pyhton RSS reader

## How to install:
**1st way**
* You need to have git installed. Run:
> $ git clone https://github.com/kirill-stp/FinalTaskRssParser.git
* when you are in your workspace folder. Then run:
> $ python setup.py install
* when you are in **final task** folder
**2nd way:**
* To install this package, you must have Python added to your user environment.
* Download the distribution archive
* run $ pip install ./python_rss_reader-1.0.tar.gz  

## Usage:
This app provide following interface:
```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     [--date DATE]
                     source

Pure Python command-line RSS reader

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose
  --limit LIMIT  Limit news topics
  --date DATE    Read news from given date (YMD)
```
for example:
> $ python3 rss_reader.py https://news.yahoo.com/rss --date 20191120 --limit 2 --verbose --json

## JSON structure:
```shell
{'Article 1': {'date':time.struct_time,
               'images': {'image desription': 'url'},
               'link': '',
               'summary': '',
               'title': ''},
 'Article 2': {date': time.struct_time,
               'images': {'image desription': 'url'},
               'link': '',
               'summary': '',
               'title': ''},
 'Feed': 'Feeds from 'url'',
 'Link': 'rss link'}

```
## Local news storage:
When **--date** argument is not provided, the news that you received will be saved to the database, if it wasn’t there yet.
Cached data stored in rss_reder/cached_feeds.db file using **shelve**. Database stores dictionary-like object, where the key is the publication date and the value is instance of **Article** class.

## HTML and PDF converting:
You can use **--to-html** and **--to-pdf** to save feed in given format. If there is no internet connection, it will paste image links (clickable in pdf). If we have internet connection, then program will download images and paste it to the file. Titles in pdf also clickable.

## Colorizing
This program can colorize normal and json output, using **termcolor**. To add some color to your life, use **--colorize** argument
 