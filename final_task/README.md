RSS-reader
=============================
Pure Python command-line RSS reader.

INSTALLATION
------------
First of all open command line and install setuptools, just write 'pip install -u setuptools'.
After that you can install our app, enter 'python setup.py install' in command line opened as an administrator
in folder final_task, where setup.py is lying.
By this point if you want to launch the application, enter 'rss-reader [arguments]'.

For work with conversion, in your folder rss_reader should be ARIALUNI.ttf.

USING
------------
rss_reader.py [--help] [--source SOURCE] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-html PATH]
              [--to-pdf TO_PDF]


positional arguments:

  source         RSS url

optional arguments:

  -h, --help         show this help message and exit

  --limit LIMIT      Limit news topics if this parameter provided

  --version          Print version info

  --json             Print result as JSON in stdout

  --verbose          Outputs verbose status messages

  --date             Print the new from the specified day, YYYYMMDD format

  --to-html TO_HTML  Convert news in html format, need path, where the file
                     will be saved

  --to-pdf TO_PDF    Convert news in pdf format, need path, where the file
                     will be saved

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

CONVERTING TO HTML OR PDF FORMAT
------------
You can download news in one of those formats, news can be read from the website or from the cache.
For doing that you should enter directory, and if it's correct, news will be converted and you will see a message,
which tells, if converting was successful or not.
In prepared file (it is named news.pdf or news.html) will be all information about news, if there is no connection
to the Internet, instead of image there will be url of it.