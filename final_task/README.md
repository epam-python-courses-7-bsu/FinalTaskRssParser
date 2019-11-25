# RSS reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable
format.

[The source for this project is available here](https://github.com/AnnaPotter/FinalTaskRssParser).


### Installation
$ pip install rss-reader-Anna-Gonchar

### Usage
$ rss-reader (-h | --help)

    Show help message and exit

$ rss-reader <RSS-SOURCE-LINK>

    Print rss feeds in human-readable format

$ rss-reader --version

    Print version info

$ rss-reader --json

    Print result as JSON in stdout

$ rss-reader.py --verbose

    Outputs verbose status messages
    
$ rss-reader.py --limit LIMIT

    Limit news topics, if this parameter provided
    
$ rss-reader.py --date DATE

    Gets a date in %Y%m%d format. Print news from the specified date
    and source (<RSS-SOURCE-LINK>), if it specified

$ rss-reader.py --to-pdf PATH_TO_PDF

    Gets file path. Convert news to pdf and save them to pdf file on the specified path

$ rss-reader.py --to-html PATH_TO_HTML

    Gets file path. Convert news to html and save them to html file on the specified path

### Storage
All the pieces of news received from the source are saved to the binary file.
Shelve module is used for this. It saves object with the specific key to the file.
The key is the rss news publication date, the value is the news.

