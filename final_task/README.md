# Console RSS Reader
Cli-based RSS Reader built with Python 3.8. 
Supports all RSS standards, can handle incorrect RSS. 
Also partially supports Atom feeds. 

## Getting Started
### Prerequisites
- Python 3.8
- feedparser, lxml, beautifulsoup4

```
pip install feedparser lxml beautifulsoup4
```
### Usage
The program runs from file `rss_parser.py`
```
usage: rss_reader.py [-h] [--version] [--json] [-v] [--limit LIMIT] source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  -v, --verbose  Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
```
### Licence
This project is licensed under the MIT License - see the LICENSE file for details.
