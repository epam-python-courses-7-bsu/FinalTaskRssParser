# RSS reader
Python command line RSS-reader.

## Usage

```shell
$ rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

Pure python command-line RSS reader

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

```

## Installation
* For installation you need setuptools

```shell
python -m pip install source_name
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