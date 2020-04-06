# RSS_READER
---------------------------------------------------------------------------
RSS reader is a command-line utility.  

### Usage
---------------------------------------------------------------------------
usage: rss_reader.py [source] [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-pdf PATH] [--to-html PATH] [--colorize]  

Pure Python command-line RSS reader.  

positional arguments:  
 - source            *RSS URL*  
  
optional arguments:  
 - -h, --help            *show this help message and exit*  
 - --version            *Print version info*  
 - --json            *Print result as JSON in stdout*  
 - --verbose            *Output verbose status messages*  
 - --limit LIMIT            *Limit news topics if this parameter provided*  
 - --date DATE            *News from the specified day will be printed out. Format: YYYYMMDD*  
 - --to-pdf PATH            *Create PDF file with news*  
 - --to-html PATH            *Create HTML file with news*  
 - --colorize            *Print news in colorized mode (not for json mode)*  

It is mandatory to specify date or/and source.  
If both are specified, then news will be searched by date and by source.  

### Json structure
---------------------------------------------------------------------------
{  
            "feed": [feed],  
            "items": [  
                        {  
                                    "title": [title],  
                                    "date": [date],  
                                    "link": [link],  
                                    "text": [text],  
                                    "image links": [  
                                                [link1], [link2], ...  
                                    ]  
                        },  
                        ...  
            ]  
}

### Local storage
---------------------------------------------------------------------------
All read news is saved in storage file *news.data*.  
When using the --date argument, news is searched by specified date from *news.data*.  

### How to install application
---------------------------------------------------------------------------
 - To install application you should have setuptools. Open cmd and enter 'pip install -U setuptools'.  
 - Use 'python setup.py install' in cmd to install application.  
 - You are now ready to run the application. Use 'rss-reader [arguments]' to run it.  
 
Warning: If path to rss-reader is not in Path variable, use full path to file at running.  