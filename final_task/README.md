# RSS reader
Python command line RSS-reader.


## Installation

* Be sure that python version is 3.8+
* For installation you need setuptools `python -m pip install setuptools`
* Download source code and use `python setup.py install`


## Usage

```
$ rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to_html PATH] [--to_pdf PATH] source

Pure python command-line RSS reader

positional arguments:
  source         RSS URL 

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date         Read cached news for provided URL. If "ALL" provided in source instead of URL - prints all cached news for this date
  --to_html      Convert news to HTML and save it in PATH
  --to_pdf       Convert news to pdf and save it in PATH

```


## JSON structure

```
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

## Cache

* Cache is saved using pickle module
* It is stored in separate file for each date named `"cache/publication_date".cache` 
* It has the next structure: `{url1: set(article1, article2, ...), url2: set(article, ...), ...}`
* Cache is currently stored in `'/tmp/rss_reader/cache'`

## Format converter

* The reader is able to convert news into HTML and pdf formats
* Jinja2 is used to convert data to html, weasyprint - to pdf

### RSS reader works correctly at least with the next URLs: 

* https://news.yahoo.com/rss/
* https://news.tut.by/rss/
* https://www.rt.com/rss/
* https://news.yandex.ru/science.rss
* https://www.theguardian.com/world/rss
* http://feeds.bbci.co.uk/news/world/europe/rss.xml
* https://rss.nytimes.com/services/xml/rss/nyt/World.xml
* https://naviny.by/rss/inter.xml
* https://eng.belta.by/rss
* https://news.rambler.ru/rss/world/
* https://lenta.ru/rss
* https://www.vesti.ru/vesti.rss]
