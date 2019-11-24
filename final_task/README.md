


#  RSS Reader v.5.0, Evgeny Androsik (androsikei95@gmail.com)

**1-5** iterations.
1. [Creation and Installation](#creation-and-installation)  
	1.1. [Package creation](#package-creation)  
	1.2. [Package installation](#package-installation)  
3. [Application launch](#application-launch)  
	2.1. [Direct launch](#direct-launch)  
	2.2 [Launch as CLI utility](#launch-as-cli-utility)  
4. [Usage](#usage)  
5. [Examples](#examples)  
	4.1.  [Direct launch examples](#direct-launch-examples)  
	4.2.  [CLI utility examples](#cli-utility-examples)  
6. [About project](#about-project)  
	6.1. [Project Structure](#project-structure)  
	6.2 [Iteration 1](#iteration-1-rss-reader.)  
	6.3 [Iteration 2](#iteration-2-distribution)  
	6.4 [Iteration 3](#iteration-3-news-caching)  
	6.5 [Iteration 4](#iteration-4-format-converter)  
	6.6 [Iteration 5](#iteration-5-output-colorization)

##  Creation and Installation

###  Package creation

 Creating package using `setup.py`:  

1. Go to the */final_task* folder wich has `setup.py` file  
	**Windows**: Run the following code: `python setup.py sdist --formats=zip`  
	**Linux**: Run the following command: `sudo python3 setup.py sdist --formats=zip`   
2. The zip package will be inside `../final_task/dist` folder.  

### Package installation

####  WINDOWS:

1. Run Console with administrator privileges (run as Administrator).  
2. In console go to directory with rss-reader-5.0.zip package.  
3. Run the following command: `pip install rss-reader-5.0.zip`  

#### LINUX

1. In console go to directory with *rss-reader-5.0.zip* package.
2. Run the following command: `sudo pip3 install rss-reader-5.0.zip`.

## Application launch

1. [Direct launch](#direct-launch)  
2. [Launch as CLI utility](#launch-as-cli-utility)  

### Direct launch

#### Requirements:
To run this app directly you need to install this external python libraries in your environment:  
1. feedparser (**Windows**: `pip install feedparser` **/** **Linux**: `sudo pip3 install feedparser`)  
2. bs4 (**Windows**: `pip install bs4` **/** **Linux**: `sudo apt-get install python3-bs4`)  
3. dateutil (**Windows**: `pip install python-dateutil` **/** **Linux**: `
sudo apt-get install python3-dateutil`)  
4. fpdf [https://pypi.org/project/fpdf/](https://pypi.org/project/fpdf/)  
5. jinja2 [https://pypi.org/project/Jinja2/](https://pypi.org/project/Jinja2/)  
6. colorama [https://pypi.org/project/colorama/](https://pypi.org/project/colorama/)  
7. termcolor [https://pypi.org/project/termcolor/](https://pypi.org/project/termcolor/)  
8. coloredlogs [https://pypi.org/project/coloredlogs/](https://pypi.org/project/coloredlogs/)  

#### Launching  
1. Open console in folder with `rss_reader.py` file.  
2. Run rss_reader.py with arguments:  
+ **Windows**: `python rss_reader.py [arguments]`  
+ **Linux**: `sudo python3 rss_reader.py [arguments]`  
Check [usage](#usage)  for arguments description. Check [here](#direct-launch-examples) for examples.  

### Launch as CLI utility

1. [Install package](#package-installation) `rss-reader-5.0.zip`  
2. Open console and run rss-reader utility with arguments:  
+ **Windows**: `rss_reader [arguments]`  
+ **Linux**: `sudo rss_reader.py [arguments]`  
Check [usage](#usage)  for arguments description. Check [here](#cli-utility-examples) for examples.  


## Usage  
Usage: `rss_reader.py [-h] [ --version ] [ --json ] [ --verbose ] [ --limit LIMIT ] [--date DATE ] [--to-html TO_HTML] [--to-pdf TO_PDF] [--colorize] source`  

+ Positional arguments:

|    Argument    |      Description              |
|----------------|-------------------------------|
|`source`        |RSS URL                        |

+ Optional arguments:

|    Argument       |      Description                                             |
|-------------------|--------------------------------------------------------------|
|`-h`, `--help`     |Show help message and exit                                    |
|`--version`        |Print version info and complete it's work                     |
|`--json`           |Print result as JSON in stdout                                |
|`--verbose`        |Outputs verbose status messages(Logs in stdout)               |
|`--limit LIMIT`    |Limit news topics if this parameter provided                  |
|`--date DATE`      |Prints the cashed news from the specified day. Format - %Y%m%d|
|`--to-html TO_HTML`|Converts news to html                                         |
|`--to-pdf TO_PDF`  |Converts news to html                                         |
|`--colorize`       |Prints the result of the utility in colorized mode.           |  
## Examples
1.  [Direct launch examples](#direct-launch-examples).  
2.  [CLI utility examples](#cli-utility-examples).  

#### Direct launch examples:

1. * **Windows:** `python rss_reader.py https://news.yahoo.com/rss/`  
    * **Linux:** `sudo python3 rss_reader.py https://news.yahoo.com/rss/`  
	Prints all RSS articles from https://news.yahoo.com/rss/  
2. * **Windows:** `python rss_reader.py https://news.yahoo.com/rss/ --limit 5`  
    * **Linux:** `sudo python3 rss_reader.py https://news.yahoo.com/rss/ --limit 5`  
	Prints 5 RSS articles from https://news.yahoo.com/rss/  
3. * **Windows:** `python rss_reader.py https://news.yahoo.com/rss/ --limit 5 --json`  
    * **Linux:** `sudo python3 rss_reader.py https://news.yahoo.com/rss/ --limit 5 --json`  
	Prints 5 RSS articles from https://news.yahoo.com/rss/ in json format  
4. * **Windows:** `python rss_reader.py https://news.yahoo.com/rss/ --verbose`  
   * **Linux:** `sudo python3 rss_reader.py https://news.yahoo.com/rss/ --verbose`  
	Prints all articles from https://news.yahoo.com/rss/, also prints logs in stout  
5. * **Windows:** `python rss_reader.py --help`  
   * **Linux:** `sudo python3 rss_reader.py --help`  
	Prints help message  
6. * **Windows:** `python rss_reader.py --version`  
   * **Linux:** `sudo python3 rss_reader.py --version`  
	Prints version of the app  
7. * **Windows:** `python rss_reader.py --date 20191111`  
   * **Linux:** `sudo python3 rss_reader.py --date 20191111`  
	The news from the specified day will be printed out
8. * **Windows:** `python rss_reader.py https://news.yahoo.com/rss/ --date 20191111`  
   * **Linux:** `sudo python3 rss_reader.py https://news.yahoo.com/rss/ --date 20191111`  
	The news from the specified day and link will be printed out 
	
#### CLI utility examples:

1. * **Windows:** `rss_reader.py https://news.yahoo.com/rss/`  
   * **Linux:** `sudo rss_reader.py https://news.yahoo.com/rss/`  
	Prints all RSS articles from https://news.yahoo.com/rss/  
2. * **Windows:** `rss_reader.py https://news.yahoo.com/rss/ --limit 5`  
   * **Linux:** `sudo rss_reader.py https://news.yahoo.com/rss/ --limit 5`  
	Prints 5 RSS articles from https://news.yahoo.com/rss/  
3. * **Windows:** `rss_reader.py https://news.yahoo.com/rss/ --limit 5 --json`  
   * **Linux:** `sudo rss_reader.py https://news.yahoo.com/rss/ --limit 5 --json`  
	Prints 5 RSS articles from https://news.yahoo.com/rss/ in json format  
4. * **Windows:** `python https://news.yahoo.com/rss/ --verbose`  
   * **Linux:** `sudo rss_reader.py https://news.yahoo.com/rss/ --verbose`  
	Prints all articles from https://news.yahoo.com/rss/, also prints logs in stout  
5. * **Windows:** `rss_reader.py --help`  
   * **Linux:** `sudo rss_reader.py --help`  
	Prints help message  
6. * **Windows:** `rss_reader.py --version`  
   * **Linux:** `sudo rss_reader.py --version`  
	Prints version of the app  
7. * **Windows:** `rss_reader.py --date 20191111`  
   * **Linux:** `sudo rss_reader.py --date 20191111`  
	The news from the specified day will be printed out
8. * **Windows:** `rss_reader.py https://news.yahoo.com/rss/ --date 20191111`  
   * **Linux:** `sudo rss_reader.py https://news.yahoo.com/rss/ --date 20191111`  
	The news from the specified day and link will be printed out 

## About project  

###  Project Structure  

```
📁final_task
├── 📁rss-reader
│   ├── __init__.py
│   ├── argparse_handler.py
│   ├── articles_handler.py
│   ├── html_converter.py
│   ├── pdf_converter.py
│   ├── colorizing_handler.py
│   ├── custom_error.py
│   ├── rss_reader.py
│   ├── single_article.py
│   ├── 📁tests
│   │   ├── __init__.py
│   │   └── test_module_1.py
│   ├── 📁templates
│   │   ├── base.html
│   │   └── style.css
│   └── 📁font
│       └── dejavusans.ttf
├── __init__.py
├── MANIFEST.in
├── FinalTask.md
├── README.md
└── setup.py
```

### [Iteration 1] RSS reader.  

### [Iteration 2] Distribution

Utility was wrapped into distribution package with setuptools . This package can be exported as CLI utility named rss-reader .

### [Iteration 3] News caching  

The news cache saving in `cache.json` file in json format.
`dateutil` - powerful extensions to datetime
I'm using `dateutil.parser` to parse dates from cache to datetime.datetime.

 `--date DATE` also works with `source`, `--json`, `--limit LIMIT`, `--verbose`  

Example:
```
"[
  {
    "feed": "Yahoo News - Latest News & Headlines",
    "feed_url": "https://news.yahoo.com/rss/",
    "title": "Is Nikki Haley auditioning to replace Pence on Trump's 2020 ticket?",
    "date": "Tue, 12 Nov 2019 11:34:28 -0500",
    "link": "https://news.yahoo.com/nikki-haley-book-tour-audition-vp-pence-trump-2020-ticket-163428688.html",
    "summary": "[image 1: Is Nikki Haley auditioning to replace Pence on Trump's 2020 ticket?][1] Less than three months ago, the former U.S. ambassador to the United Nations tried to tamp down speculation that she might replace the vice president on Trump’s 2020 ticket. But multiple political observers say her new book tour is doubling as an audition for the role.",
    "links": [
      "[1]: http://l2.yimg.com/uu/api/res/1.2/XnMA9mstMRV0FkOdMugjhg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/f1884750-fcd3-11e9-bcf7-cef09bc7ad91",
      "[2]: https://news.yahoo.com/nikki-haley-book-tour-audition-vp-pence-trump-2020-ticket-163428688.html"
    ]
  },
  {
    "feed": "CNN.com - RSS Channel - World",
    "feed_url": "http://rss.cnn.com/rss/edition_world.rss",
    "title": "Israel's military campaign against Islamic Jihad enters second day",
    "date": "Tue, 12 Nov 2019 16:44:31 GMT",
    "link": "http://rss.cnn.com/~r/rss/edition_world/~3/zbNZA-KiPFo/index.html",
    "summary": "Twenty-four Palestinians, among them 17 militants and a seven-year-old boy, have been killed by Israeli air strikes in Gaza since fighting began Tuesday morning, according to Palestinian health officials.[image 1: no description][1] ",
    "links": [
      "[1]: http://feeds.feedburner.com/~r/rss/edition_world/~4/zbNZA-KiPFo",
      "[2]: http://rss.cnn.com/~r/rss/edition_world/~3/zbNZA-KiPF/inde.html"
    ]
  }
]"
```  
`python rss_reader.py --date 20191112` will print both articles  
`python rss_reader.py https://news.yahoo.com/rss/ --date 20191112` will print first article  

### [Iteration 4] Format converter  

Two more arguments was added: `--to-html PATH`, `--to-pdf PATH`  
Works with URL: `python rss_reader.py https://news.yahoo.com/rss/ --to-html D: --to-pdf C:`  
Works with date: `python rss_reader.py https://news.yahoo.com/rss/ --date 20191116 --to-html D:`  

For pdf creation FPDF module was used.  

If Internet conection is on images will be loaded, else only URL's.  

### [Iteration 5] Output colorization  

**colorama** and **termcolor** was used to colorize output
**coloredlogs** was used to colorize logs

### [Iteration 6] Web-server  


## For fast use
```
python rss_reader.py "https://news.yahoo.com/rss/"
python rss_reader.py "https://news.tut.by/rss/economics.rss"
python rss_reader.py 'http://rss.cnn.com/rss/edition_world.rss'
python rss_reader.py http://feeds.bbci.co.uk/news/rss.xml?edition=uk
python rss_reader.py "http://billmaher.hbo.libsynpro.com/rss"
python rss_reader.py "https://www.craigslist.org/about/best/all/index.rss"
```
`coverage run --source=. -m unittest discover -s .\tests`