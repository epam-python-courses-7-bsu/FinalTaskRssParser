# RSS reader
Python command line RSS-reader.

## Usage

```shell
$ rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] source

Pure python command-line RSS reader

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date         Read cached news for provided URL. If "ALL" provided - prints all cached news for this date

```

## Installation
Be sure that python version is 3.7+
For installation you need setuptools

```shell
python -m pip install setup.py
```

To launch the app you need to type
```shell
$ rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] source
```


## JSON structure
```shell
{
    "news_outlett_name": "news outlett name",
    "news_title": "news title",
    "pub_date": "publication date, Sun, 17 Nov 2019 10:44:20 -0500",
    "news_link": "news link",
    "news_description": "news description",
    "img_alt": "image alternative if exist",
    "img_src": "image link if exist",
}
```

### RSS reader works correctly at least with the next URLs: 

https://news.yahoo.com/rss/
https://news.tut.by/rss/
https://www.rt.com/rss/
https://www.theguardian.com/world/rss
http://feeds.bbci.co.uk/news/world/europe/rss.xml
https://rss.nytimes.com/services/xml/rss/nyt/World.xml
https://naviny.by/rss/inter.xml
https://eng.belta.by/rss
https://news.rambler.ru/rss/world/
https://lenta.ru/rss
https://www.vesti.ru/vesti.rss
  