
This program which receives RSS URL and prints results in human-readable
format.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     Show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    To search in cache for news by date in the format in YYYYmmdd



Installation recommendation rss-reader:
1)Open terminal 
2)Enter "pip install setuptools" or "pip3 install setuptools"
3)Go to the folder final_task
4)Enter "python3 setup.py install"
5)Application installed
6)To run the utility, type in the terminal "rss-reader" then a space and url on news
Example : rss-reader  https://news.yahoo.com/rss

News caching: 
In order to see the history you must enter an additional parameter --date
Example: rss-reader https://news.tut.by/rss/ --limit 2 --date 20191122
Searching by date and source

Format converter:
1)Use --to-pdf to save news in pdf format
2)Use --to-html to save news in html format
3)If no internet connection, get a file without images
4)Enter the full path to the file 
5)If you enter path to directory,news successfully saved to file "your path+News.(pdf or html)"







