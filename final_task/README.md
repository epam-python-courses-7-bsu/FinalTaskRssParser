
#  RSS Reader v.2.0, Evgeny Androsik (androsikei95@gmail.com)

**First** and **second** iterations.
1. [Creation and Installation](#creation-and-installation)
	1.1. [Package creation](#package-creation)
	1.2. [Package installation](#package-installation)
3. [Application launch](#aapplication-launch)
	2.1. [Direct launch](#direct-launch)
	2.2 [Launch as CLI utility](#launch-as-cli-utility)
4. [Usage](#usage)
5. [Examples](#examples)
	4.1.  [Direct launch examples](#direct-launch-examples).
	4.2.  [CLI utility examples](#cli-utility-examples).

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
2. In console go to directory with rss-reader-2.0.zip package.
3. Run the following command: `pip install rss-reader-2.0.zip`

#### LINUX

1. In console go to directory with *rss-reader-2.0.zip* package.
2. Run the following command: `sudo pip3 install rss-reader-2.0.zip`.

## Application launch

1. [Direct launch](#direct-launch)
2. [Launch as CLI utility](#launch-as-cli-utility)


### Direct launch

#### Requirements:
To run this app directly you need to install this external python libraries in your environment:
1. feedparser (**Windows**: `pip install feedparser` **/** **Linux**: `sudo pip3 install feedparser`)
2. bs4 **(Window**s: `pip install bs4` **/** **Linux**: `sudo pip3 install bs4`)

#### Launching
1. Open console in folder with `rss_reader.py` file.
2. Run rss_reader.py with arguments:
+ **Windows**: `python rss_reader.py [arguments]`
+ **Linux**: `sudo python3 rss_reader.py [arguments]`
Check [usage](#usage)  for arguments description. Check [here](#direct-launch-examples) for examples.

### Launch as CLI utility

1. [Install package](#package-installation) `rss-reader-2.0.zip`
2. Open console and run rss-reader utility with arguments:
+ **Windows**: `rss_reader [arguments]`
+ **Linux**: `sudo rss_reader.py [arguments]`
Check [usage](#usage)  for arguments description. Check [here](#cli-utility-examples) for examples.


## Usage
Usage: `rss_reader.py [-h] [ --version ] [ --json ] [ --verbose ] [ --limit LIMIT ] source`

+ Positional arguments:

|    Argument    |      Description              |
|----------------|-------------------------------|
|`source`        |RSS URL                        |

+ Optional arguments:

|    Argument   |      Description                               |
|---------------|------------------------------------------------|
|`-h`, `--help` |Show help message and exit                      |
|`--version`    |Print version info and complete it's work       |
|`--json`       |Print result as JSON in stdout                  |
|`--verbose`    |Outputs verbose status messages(Logs in stdout) |
|`--limit LIMIT`|Limit news topics if this parameter provided    |

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

##  Project Structure

```
📁final_task
├── 📁rss-reader
│   ├── __init__.py
│   ├── custom_error.py
│   ├── rss_reader.py
│   ├── single_article.py
│   └── 📁tests
│       ├── __init__.py
│       └── test_module_1.py
├── __init__.py
├── FinalTask.md
├── README.md
└── setup.py
```