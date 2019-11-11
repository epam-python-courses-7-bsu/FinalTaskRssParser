# RSS_READER
---------------------------------------------------------------------------
RSS reader is a command-line utility.

### Usage
---------------------------------------------------------------------------
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.
positional arguments:
source RSS URL
optional arguments:
    -h, --help show this help message and exit
    --version Print version info
    --json Print result as JSON in stdout
    --verbose Outputs verbose status messages
    --limit LIMIT Limit news topics if this parameter provided

### Json structure
---------------------------------------------------------------------------
{
    "feed": [feed],
    "items": [
        {
            "title": [title],
            "date": [date],
            "link": [link],
            "text": [text],
            "image links": [
                [link1], [link2], ...
            ]
        },
        ...
    ]
}