# RSS reader

### Installation

1) from the source distribution,

- download the [zipped folder](https://github.com/AntonZimahorau/FinalTaskRssParser/tree/master/final_task/dist/rss_reader_Anton_Zimahorau-2.2.tar.gz), then:

	$ pip install ./rss_reader_Anton_Zimahorau-2.2.tar.gz

### Usage

`$ rss-reader (-h | --help)`

- Show help message and exit

`$ rss-reader <RSS-LINK>`

- Print rss feeds in human-readable format

`$ rss-reader --version`

- Print version info

`$ rss-reader --json`

- Print result as JSON in stdout

`$ rss-reader.py --verbose `

- Outputs verbose status messages

`$ rss-reader.py --date DATE`

- Take a date in %%Y%%m%%d format. Print cached news, published on this date.
  If source argument passed, print only news from this source

`$ rss-reader.py --limit LIMIT`

- Limit news topics if this parameter provided

`$ rss-reader.py --to-epub TO_EPUB`

- Create a book in epub format from internet
source or database. Receive the path where file will be saved

`$ rss-reader.py --to-html TO_HTML`

-Create a file in html format from internet
source or database. Receive the path where file will be saved

`$ rss-reader.py --colorize`

-Print the result of the utility in colorized mode

### JSON structure:

```
{
"news": [
     {
       "title": "News title",
       "date": "Publishing date",
       "link": "News link",
       "text": "Text content of news",
       "links": ["links that presented in text",],
       "feed_title": "Feed title"
       "source": "source url"
     },
     {
       "title": "News title",
       "date": "Publishing date",
       "link": "News link",
       "text": "Text content of news",
       "links": ["links that presented in text",],
       "feed_title": "Feed title"
       "source": "source url"
     },
     {
        ...
     }
	    ]
}
```

### News storage
>For news storage a “shelve”, persistent, dictionary-like object was used.
>"Shelve object will be situated in your home directory. 
>All fetched news will be saved in "shelve" object.
>The keys for search is a rss publication date string. 
>The values is python News() objects.
>More information about "shelve" is avaliable on [link](https://docs.python.org/3/library/shelve.html).
