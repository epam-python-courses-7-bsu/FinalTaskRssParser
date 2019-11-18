# **Rss-reader**
Command-line utility to receive RSS feeds, save it and convert to common formats.


## **Example**

Input:
```
python3 rss_reader.py https://news.yahoo.com/rss - -limit 1
```
Output:
```
Title : Rep. Justin Amash turned on Trump. Will his Michigan district follow him — or turn on him?

Date : Sun, 17 Nov 2019 06:00:35 -0500

Link : https://news.yahoo.com/rep-justin-amash-turned-on-trump-will-his-michigan-district-follow-him-or-turn-on-him-110017880.html

Description : If you want to understand how impeachment is being seen by actual Americans, 
there may be no better place to go than Grand Rapids, Mich. In part that’s because 
the area around Grand Rapids, comprising Michigan’s Third Congressional District,
is one of only about two dozen districts in the nation to vote for Barack Obama and for Donald Trump.
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





