# Pyhton RSS reader

## How to install:
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
Cached data stored in rss_reder/cached_feeds.db file using **shelve**. Database stores dictionary-like object, where the key is the publication date and the value is object of **Article** class.

