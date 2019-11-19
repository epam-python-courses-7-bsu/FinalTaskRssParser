# Python RSS parser
***
Yet another RSS parser
***
# Quick start

## Usage
    usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [url]

    RRS feed receiver

    positional arguments:
    url            URL for RSS feed

    optional arguments:
    -h, --help     show this help message and exit
    --version      prints version
    --json         converts news to JSON
    --verbose      output verbose status messages
    --limit LIMIT  determines the number of showed news.
    --date DATE    shows cached news at given date
## Installation
1. Install setuptools

        pip install setuptools
2. Download source code
3. Unpack downloaded *.zip
4. Go to `FinalTaskRssParser-master/final_task`
5. In terminal execute:
    
        python setup.py install

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
        "link": "link",
        "media": "media",
        "published": "date",
        "title": "title"
    }

## Caching
TinyDB have been used for caching.

Items are stored in json format.
News are stored in db.
##### Database item format
    "id": {
            "date": "date",
            "link": "link",
            "media": "media",
            "published": "published",
            "source": "source",
            "title": "title"
        },
`date` is stored in format `yyyy%mm%dd`