# RSS reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable
format.

[The source for this project is available here](https://github.com/AnnaPotter/FinalTaskRssParser).


### Installation
$ pip install rss-reader-Anna-Gonchar

### Storage
All the pieces of news received from the source are saved to the binary file.
Shelve module is used for this. It saves object with the specific key to the file.
The key is the rss news publication date, the value is the news.

