# RSS-READER

## What is rss-reader?

This is small application for watching feed on your device. It shows shot information about the latest news and keeps previous news.

## How to instal?

1. To install the application on your device must be python 3.7 and more.
2. Download this repository on your device.
3. Open command line(Terminal) in this directory.
4. Enter next command:
```
python setup.py sdist
cd dist
pip install feedparser
pip install rss-reader-3.6.tar.gz
```
5. Check workability with command: 
```
rss-reader -h
```

## Parameters:
```
usage: rss-reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] source

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Obtaining the cached news without the Internet
```
