RSS_READER
RSS reader is a command-line utility.

Usage
usage: rss_reader.py [-h] [--source SOURCE] [--version] [--json] [--verbose]
[--limit LIMIT] [--date DATE]

Pure Python command-line RSS reader.

optional arguments:

-h, --help            show this help message and exit
--source SOURCE            RSS URL
--version            Print version info
--json            Print result as JSON in stdout
--verbose            Outputs verbose status messages
--limit LIMIT            Limit news topics if this parameter provided
--date DATE            News from the specified day will be printed out. Format: YYYYMMDD
It is mandatory to specify date or/and time.
If both are specified, then news will be searched by date and by source.

Json structure
[
    {
            "feed": [feed],
            "title": [title],
            "date": [date],
            "link": [link],
            "text": [text],
            "image links": [
                [link1]
                [link2]
                ...
            ]
    },
        ...
]

Local storage
All read news is saved in database by using Mysql. You should have database final_task_database with table news_cache
new-cache structure:
    feed:longtext
    title:longtext
    date:date
    link:longtext
    image_description:longtext
    new_description:longtext
    image_links:longtext
When using the --date argument, news is searched by date in database

How to install application
To install application you should have setuptools. Open cmd and enter 'pip install -U setuptools'.
Using 'pyhton setup.py install' in cmd install application.
Install requirements 'pip install -r requirements.txt'
You are now ready to run the application. Use 'rss-reader [arguments]' to run it.
Warning: If path to rss-reader is not in Path variable, use full path to file at running.