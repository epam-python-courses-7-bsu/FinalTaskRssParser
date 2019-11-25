# RSS Reader
Cli-based RSS reader built with Python 3.8. 
Supports all RSS standards, can handle incorrect RSS. 
Also partially supports Atom feeds. 

## Getting Started
### Prerequisites
- Python 3.8
- feedparser, lxml, beautifulsoup4

```
pip install feedparser lxml beautifulsoup4
```
### Installation
```
pip install -i https://test.pypi.org/simple/ rss-reader-scarzdz
```
Also you can just download source code and install using: 
```
$ python final_task/setup.py install
```
### Running
After installation, `rss-reader` command is added to PATH.

Alternatively, the application can be run from the source file:
``` 
$ cd final_task
$ python -m rss_reader ...
```
### Usage
```
usage: rss-reader [-h] [--version] [--json] [-v] [--limit LIMIT] source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  -v, --verbose  Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Load news with date (%Y%m%d) from cache, if this parameter
                 provided
```
## Behavior
RSS Reader can work in online or offline mode. 

In **online** mode, when `--date` argument is not provided, the application loads and parses rss feed from `source` argument. 
It is done using `feedparser` library. 
Parsed news saved in **_sqlite database_**, which located in `rss_parser/data/rss.sqlite`. 
If item contains _html_ markup, it converted to plain text.

In **offline** mode, when `--date` argument is provided, 
the application loads news with specified feed link and date from the database.

News printed to stdout in the following format:

```
Feed: *RSS feed title*


Title: *item 1 title*
Date: *%a, %d %b %Y %H:%M:%S +0000* 
Link: https://example.com/link_to_item

*Item description*

Links:
[1]: *first link is always link to item*
[2]: Others can be links parsed from  <a> or <img> tags


Title: *item 2 title*
Date: ...
```

News is converted to json like this:
```
{
  "title": "*Feed title*",
  "link": "*link to feed*"
  "items": [
    {
      "title": "*item 1 title*",
      "date": *time.struct_time tuple*,
      "link": "*link to item*",
      "enclosure": *null* or *link to eclosure*,
      "description": "*item description*",
      "description_parsed": "*description parsed to plain text*"  or *null* if description is text
    },
    ...
  ]
}
```

## Licence
This project is licensed under the MIT License - see the LICENSE file for details.
