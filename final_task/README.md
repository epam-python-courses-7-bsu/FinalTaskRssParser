# Python RSS parser
***
Yet another RSS parser
***
# Quick start

## Usage
    rss_reader.py --help
    usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] url

    RRS feed receiver

    positional arguments:
    url            URL for RSS feed

    optional arguments:
    -h, --help     show this help message and exit
    --version      prints version
    --json         converts news to JSON
    --verbose      output verbose status messages
    --limit LIMIT  determines the number of showed news. Default is 3

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