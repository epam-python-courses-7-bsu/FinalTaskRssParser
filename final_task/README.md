# RSS_READER
---------------------------------------------------------------------------
RSS reader is a command-line utility.  

### Usage
---------------------------------------------------------------------------
usage: rss_reader.py [-h] [--source SOURCE] [--version] [--json] [--verbose]  
                     [--limit LIMIT] [--date DATE]  

Pure Python command-line RSS reader.  

optional arguments:  
 - -h, --help&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*show this help message and exit*  
 - --source SOURCE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*RSS URL*  
 - --version&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Print version info*  
 - --json&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Print result as JSON in stdout*  
 - --verbose&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Outputs verbose status messages*  
 - --limit LIMIT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Limit news topics if this parameter provided*  
 - --date DATE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*News from the specified day will be printed out. Format: YYYYMMDD*  

It is mandatory to specify date or/and time.  
If both are specified, then news will be searched by date and by source.  

### Json structure
---------------------------------------------------------------------------
{  
&nbsp;&nbsp;&nbsp;&nbsp;"feed": [feed],  
&nbsp;&nbsp;&nbsp;&nbsp;"items": [  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"title": [title],  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"date": [date],  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"link": [link],  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"text": [text],  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"image links": [  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[link1], [link2], ...  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  
&nbsp;&nbsp;&nbsp;&nbsp;]  
}

### Local storage
---------------------------------------------------------------------------
All read news is saved in storage file *news.data*.  
When using the --date argument, news is searched by specified date from *news.data*.  

### How to install application
---------------------------------------------------------------------------
 - To install application you should have setuptools. Open cmd and enter 'pip install -U setuptools'.  
 - Using 'pyhton setup.py install' in cmd install application.  
 - You are now ready to run the application. Use 'rss-reader [arguments]' to run it.  
 
Warning: If path to rss-reader is not in Path variable, use full path to file at running.  