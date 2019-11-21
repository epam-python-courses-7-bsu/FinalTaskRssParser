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
news_cache structure:
    feed:longtext
    title:longtext
    date:date
    link:longtext
    image_description:longtext
    new_description:longtext
    image_links:longtext
When using the --date argument, news is searched by date in database

Saving in format feature
You can save getted news in 2 formats: html, fb2
If news are got from Internet and Internet on news images are downloaded from website
and converted in base64 string. After saved html or fb2 format files can show them without connecting
to Internet. If Internet  off images aren't downloaded, in html instead of images utility writes links of images.
When using the --date argument, news are got from database. Image are downloaded the same way depending on whether 
the Internet is on

Colorize mode
When using the --colorize argument the output news in console will be colorized. If using --json at the same time
the output news will be printed in colorized json format

How to install application
To install application you should have setuptools. Open cmd and enter 'pip install -U setuptools'.
Using 'pyhton setup.py install' in cmd install application.
Install requirements 'pip install -r requirements.txt'
You are now ready to run the application. Use 'rss-reader [arguments]' to run it.
Warning: If path to rss-reader is not in Path variable, use full path to file at running.