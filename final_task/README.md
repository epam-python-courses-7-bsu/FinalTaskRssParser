
# Python RSS-reader
Python RSS-reader is a command-line utility which receives RSS URL and prints results in human-readable format.

To start Python RSS-reader run one of the following commands in command line:
 
 ``python rss_reader.py "https://news.yahoo.com/rss/" --limit 1``
``python rss_reader.py "https://timesofindia.indiatimes.com/rssfeedstopstories.cms" --json --limit 1``
  7 file in my project
  - consoleArgumemt.py this file which handles console phrases
  - ConsoleOut.py - in this file function which handles print to console
  - Handler.py - handles request
  - Log.py - 
  - rss-reader.py - main file in project
  - RssException.py - contains exception
  - WorkWithCache.py -  in this file function which works with cache(read and write json)
  
### JSON structure:
 ``` 
{
    "news": "news text",
    "title": "Title of news",
    "date": "Wed, 20 Nov 2019 02:47:47 -0500",
    "links": [
      "http://l1.yimg.com/uu/api/res/1.2/1KHP4ztUcOL6a98.vsEHQA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/0dca2dadd67f7128eb881f0333640fce05a84084.jpg"
    ],
    "strDate": "20191120"
    
} 
```
### Functional
```
positional arguments:
source RSS URL
optional arguments:
-h, --help show this help message and exit
--version Print version info
--json Print result as JSON in stdout
--verbose Outputs verbose status messages
--limit LIMIT Limit news topics if this parameter provided
--date - view news from cache with specified date
```

    
