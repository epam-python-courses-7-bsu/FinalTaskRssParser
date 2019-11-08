#The best RSS-reader!
Program is named rss_reader.py.

To run the program from the command line, you must write the file name and string with URL-address of news site.

Also it have such parameters like:
* --version (Print version info);
* --json (Print result as JSON in stdout);
* --verbose (Outputs verbose status messages);
* --limit LIMIT (Limit news topics if this parameter provided, type(LIMIT)=int).

It's print a brief description of the news information that appeared on the news site in human-readable
format. 

JSON format example:

```json
[
    {
        "Feed": "Yahoo",
        "Updated": "Fri, 08 Nov 2019 17:04:06 GMT",
        "Version": "rss20"
    },
    {
        "Title": "Some title",
        "Date": "Thu, 07 Nov 2019 09:59:52 -0500",
        "Summary": "Some summary",
        "Link": "Link to news",
        "Image": "Some image information"
    }
]
```

The following external libraries are used in this program:
feedparser and bs4.
