#The best RSS-reader!
Program is named rss_reader.py.
##Instalation
The recommended way to install rss-reader is with pip:
* pip install rss_reader - for Windows
* sudo pip install rss_reader - for Linux and Mac

##Description and Functions
```
usage: rss_reader.py [-h] [--limit LIMIT] [--version] [--json] [--verbose]
                     [--date DATE] [--to_pdf TO_PDF] [--to_epub TO_EPUB]
                     [source]

Pure Python command-line RSS reader.

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --limit LIMIT      Limit news topics if this parameter provided
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --date DATE        Return news from cache with that date.
  --to_pdf TO_PDF    Conversion of news in the pdf format.
  --to_epub TO_EPUB  Conversion of news in the ___ format.
```

To run the program from the command line, you must write the file name and string with URL-address of news site.

It's print a brief description of the news information that appeared on the news site in human-readable
format and save them in cache. 

Example:
```python rss_reader.py "https://news.yahoo.com/rss/" --limit 1

Feed: Yahoo News - Latest News & Headlines

Updated: Sun, 24 Nov 2019 21:19:04 GMT

Version: rss20
--------------------------------------------------------
Title: Ukraine's President Zelensky said he didn't feel pressured by Trump. Here
's why that's bogus.
Date: Sat, 23 Nov 2019 08:57:00 -0500
Link: https://news.yahoo.com/ukraines-president-zelensky-said-didnt-135700678.ht
ml
Summary:  [Image: Ukraine's President Zelensky said he didn't feel pressured by
Trump. Here's why that's bogus.] The US government's assistance to Ukraine is vi
tal as it contends with an ongoing conflict with pro-Russian separatists in the
Donbas region.
Source of image: http://l2.yimg.com/uu/api/res/1.2/3h5JxcDjAP1pHR6KUD2JMQ--/YXBw
aWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-US/business_insider_
articles_888/7a21ff2ee09c3b4285094c4e64e9602c
```
###Nice features
You can To please the eyes you can read the news from console in a colorful format.
For this enter such parameter like --colorize and enjoy.

But this parameter work only for MAC and Linux console.

###How to read saving news:
If you want to read saved news of a certain date, you must enter a --date in %Y%m%d format and the program will work
without any connecting to the Internet.

It is also possible to select news from a specific source of a certain date, for this you must enter the url-address
and --date that you want.

###What formats can you convert to? How to do it.
Program can convert news in ```--to_pdf``` and ```--to_epub``` format. 
Specify the path to the file yourself. Also program convert news in ```--json``` format
but print result as JSON in stdout.

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
#####Ways for converting:
- *You can convert from cache*

For this case news conversion is not depend on internet.
With ```rss_reader.py --date 20191117 --limit 1 --to_pdf /folder1/folder2/file_name.pdf``` one news for the specified day
would be converted (the same with ```--to_epub```) and would be generated or overwritten file 'file_name.pdf'
in folder what you choose.

- *You can convert news from the Internet*

For this case Internet is required.
With ```rss_reader.py https://news.yahoo.com/rss/ --limit 1 --to_pdf /folder1/folder2/file_name.pdf``` one news
from specified link would be converted (the same with ```--to_epub```)and would be generated or overwritten
file 'file_name.epub' in folder what you choose.



