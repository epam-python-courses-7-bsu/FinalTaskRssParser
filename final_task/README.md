RSS-reader
=============================
Pure Python command-line RSS reader.

INSTALLATION
------------
First of all open command line and install setuptools, just write 'pip install -u setuptools'.
After that you can install our app, enter 'python setup.py install' in command line to do this.
By this point if you want to launch the application, enter 'python rss-reader [arguments]'.

For working with cache you have to install PostgreSQL, you can do this from the website
https://www.postgresql.org/download/. During installation you need to enter password, use 1234 or your own,
but in this case write it in file 'password.txt', others options leave default.

USING
------------
rss_reader.py [--help] [--source SOURCE] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE]


positional arguments:

  source         RSS url

optional arguments:

  -h, --help     show this help message and exit

  --limit LIMIT  Limit news topics if this parameter provided

  --version      Print version info

  --json         Print result as JSON in stdout

  --verbose      Outputs verbose status messages

  --date         Print the new from the specified day, YYYYMMDD format

FORMAT OF PRESENTING NEWS
------------
Feed: [feed]
__________________________________________________________________
Title: [title]

Date: [date of publishing]

Link: [link of news]

[[image:  alt of image][2]description of news]   # if the image exists

[description of news]   # if doesn't

Links:

[1]: [link of news]

[2]: [link of image, if it exists]
__________________________________________________________________
...

JSON FORMAT
------------
If arguments '--json' is provided, news will be presented in json format, the structure will be like this:

[

     {

          "Feed": [feed],

          "Title": [title],

          "Date": [date of publishing],

          "Description": [description],

          "Link [1]": [link of news],

          "Link [2]": [link of image, if it exists]

     },

     ...

]

Description will be in format [[image: alt of image][2]description of news], if the image exists,
or in format [description of news], if it doesn't.