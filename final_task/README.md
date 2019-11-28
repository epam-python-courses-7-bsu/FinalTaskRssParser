# RSS-READER

## Command-line utility which receives RSS URL and prints results in human-readable format.

### **Example:**
python rss_reader.py https://news.yahoo.com/rss - -limit 1

### **Output**:

**Feed:  Yahoo News - Latest News & Headlines**

**Title**:  Families come from across U.S. to grieve relatives slain in Mexico

**Date**:  Thu, 07 Nov 2019 01:06:45 -0500

**Link**:  https://news.yahoo.com/under-armed-escort-mourner-convoys-060645935.html

**Description**:  An American man whose grandchildren were slain in a massacre in Mexico demanded justice on Thursday for other victims of the country's drug war, as relatives gathered from
across the United States for a funeral guarded by heavily armed military.  Kenneth Miller lost his daughter-in-law and four grandchildren, all dual citizens, in an ambush on Monday in th
e northern border state of Sonora that killed three mothers and six children.  The attack on members of breakaway Mormon communities who  settled in Mexico decades ago prompted U.S. Pres
ident Donald Trump to urge Mexico and the United States to "wage war" together on drug cartels.

**Links**:

```
[1]:  https://news.yahoo.com/under-armed-escort-mourner-conv... (link)
[2]:  http://l.yimg.com/uu/api/res/1.2/rRx_J3xHKYzIQ4EsiCPRT...
```

```
positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
```

## Installation

The recommended way to install rss-reader is with pip:


```
pip install rssreaderih
```

or from source distribution:

```
python setup.py install
```

## Data caching

I wrote a program that creates a database for convenient storage of news. The **postgresql** database is perfectly suited for this. Pictures are also stored in the database in binary format.

## Converting

To convert data to html format, I used the **dominate** library.

Example:
```
html_document = dominate.document(title="HTML document")

with html_document:
    with div():
        h2("Title: " + news_title)
        p("Link: " + news_link)
        p("Description: " + news_description)
```

To convert data to pdf format from html document, I used the **xhtml2pdf** library.

Example:
```
from xhtml2pdf import pisa

pdf_file = pisa.CreatePDF(sourceHtmlFile)
```

## Deploying

The application has a **dockerfile** for creating an application image. And **docker-compose.yml** file for linking application and database images.

To deploy application use this command:
```
docker-compose up
```

If you made changes to the application then use command:
```
docker-compose up --build
```
