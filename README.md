# **Rss-reader**
Command-line utility to receive RSS feeds, save it and convert to common formats.


## **h2Example**

Input:
```
python3 rss_reader.py https://news.yahoo.com/rss - -limit 1
```
Output:
```
**Feed** :

**Title** :

**Date** :

**Link** :

**Description** :
```
Help:
```
positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --data         Print news from the specified day
  --html         Convert news in HTML format
  --pdf          Condert news in PDF format
  ```

## Installation
```
pip install -r requirements.txt
pip install rss-reader
```





