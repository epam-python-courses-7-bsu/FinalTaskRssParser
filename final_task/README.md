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

`$ rss-reader.py --limit LIMIT`

- Limit news topics if this parameter provided


### JSON structure:

```
{
  "Feed": "Feed title"
  "news": [
     {
       "title": "News title",
       "date": "Publishing date",
       "link": "News link",
       "text": "Text content of news",
       "links": ["links that presented in text",]
     },
     {
       "title": "News title",
       "date": "Publishing date",
       "link": "News link",
       "text": "Text content of news",
       "links": ["links that presented in text",]
     },
     {
        ...
     }
	    ]
}
```

### News storage
>For news storage a “shelve”, persistent, dictionary-like object was used.
>More information is avaliable on [link](https://docs.python.org/3/library/shelve.html).

#### JSON structure for news from storage:

```
{
  "news": [
     { 
       "Feed": "Feed title"
       "title": "News title",
       "date": "Publishing date",
       "link": "News link",
       "text": "Text content of news",
       "links": ["links that presented in text",]
     },
     {
       "Feed": "Feed title"
       "title": "News title",
       "date": "Publishing date",
       "link": "News link",
       "text": "Text content of news",
       "links": ["links that presented in text",]
     },
     {
        ...
     }
	    ]
}
```