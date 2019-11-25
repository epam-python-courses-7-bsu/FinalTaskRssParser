# Python RSS parser
***
Yet another RSS parser
***
# Quick start

## Usage
    usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [source]

    RRS feed receiver

    positional arguments:
    source            URL for RSS feed

    optional arguments:
    -h, --help         show this help message and exit
    --version          prints version
    --json             converts news to JSON
    --verbose          output verbose status messages
    --limit LIMIT      determines the number of showed news.
    --date DATE        shows cached news at given date
    --to_pdf TO_PDF    coverts news to PDF.
    --to_html TO_HTML  coverts news to HTML.

    TO_PDF/TO_HTML - path to directory for file
    File's name is in format feed-*current datetime*.*extention*

If there are no news found while using both `--date` and `--to_pdf` or `--to_html` convertion does not happen

## Installation
1. Install setuptools

        pip install setuptools
2. Download source code
3. Unpack downloaded *.zip
4. Go to `FinalTaskRssParser-master/final_task`
5. In terminal execute:
    
        python setup.py sdist
6. Go to `/dist` directory
7. Execute `pip install rss_reader-1.4.tar.gz`

Done!
To see help use
    
    rss-reader --help

## JSON format
    {
        "description": "description",
        "link": "link",
        "news_list": [
            news_item,
            news_item,
            news_item,
            ...
        ],
        "title": "title"
    }

news_item is represented as:

    {
        "date": "date",
        "desctiption": "description",
        "img": "base64",
        "link": "link",
        "media": "media",
        "published": "published",
        "source": "source",
        "title": "title"
    }
Base64 string is pretty long, so it've been shortened to `"base64"` while printing, but it is stored as valid string in memory and cache
## Caching
TinyDB have been used for caching.

Items are stored in json format.
News are stored in db.json
##### Database item format
    "id": {
            "date": "date",
            "img": "base64_representation_of_an_image"
            "desctiption": "description",
            "link": "link",
            "media": "media",
            "published": "published",
            "source": "source",
            "title": "title"
        },
`date` is stored in format `yyyy%mm%dd`