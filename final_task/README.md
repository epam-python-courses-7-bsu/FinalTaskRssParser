# RSS-READER

## What is rss-reader?

This is small application for watching feed on your device. It shows shot information about the latest news and keeps previous news.

## How to install?

1. To install the application on your device must be python 3.7 and more.
2. Download this repository on your device.
3. Open command line(Terminal) in this directory.
4. Enter next command:
```
python setup.py sdist
cd dist
pip install feedparser
pip install requests
pip install fpdf
pip install colored
pip install rss-reader-5.1.tar.gz
```
5. Check workability with command: 
```
rss-reader -h
```

## Parameters:
```
rss-reader -h
usage: rss-reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-html TO_HTML] [--to-pdf TO_PDF] [source]

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limit news topics if this parameter provided
  --date DATE        Obtaining the cached news without the Internet
  --to-html TO_HTML  The argument gets the path where the HTML news will be saved
  --to-pdf TO_PDF    The argument gets the path where the PDF news will be saved
  --colorize         Colorize text
```

##JSON format

```
{
    "title": "Yahoo News - Latest News & Headlines",
    "items": [
        {
            "title": "Sorry, Hillary: Democrats don't need a savior",
            "published": "Wed, 13 Nov 2019 14:42:53 -0500",
            "link": "https://news.yahoo.com/sorry-hillary-democrats-dont-need-a-savior-194253123.html",
            "summary": "[image 1: Sorry, Hillary: Democrats don't need a savior][1] With the Iowa caucuses fast approaching, Hillary Clinton is just the latest in the colorful cast of characters who seem to have surveyed the sprawling Democratic field, sensed something lacking and decided that “something” might be them."
        },
        {
            "title": "Immigration officer blows whistle on 'morally objectionable' Trump asylum policy",
            "published": "Wed, 13 Nov 2019 12:09:02 -0500",
            "link": "https://news.yahoo.com/immigration-officer-blows-whistle-on-morally-objectionable-trump-asylum-policy-170902774.html",
            "summary": "[image 2: Immigration officer blows whistle on 'morally objectionable' Trump asylum policy][2] A new anonymous whistleblower has accused the Trump administration of requiring U.S. asylum officers to enforce an illegal and immoral policy “clearly designed to further this administration's racist agenda of keeping Hispanic and Latino populations from entering the United States.”"
        }
    ],
    "links": [
        "http://l.yimg.com/uu/api/res/1.2/xq3Ser6KXPfV6aeoxbq9Uw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/14586fd0-064d-11ea-b7df-7288f8d8c1a7",
        "http://l.yimg.com/uu/api/res/1.2/yNVwYmqKaLb3EZLc7wAnTw--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/173727c0-0637-11ea-afa6-2c8c926c8f7d"
    ]
}
```

* "title" - source name\
* "items" - list with dictionary which contains one news information\
    * "title" - headline news
    * "published" - date publication
    * "link" - link
    * "summary" - description
* "links" - this is a list with links to the image of the I-th news

##How is data keeping?

Data keep in local file which is located in directory:
Windows:`C:\Users\User\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\rss_reader`
Linux:\
macOS:

There is only json string in the file. JSON format: 
```
{
   "20191117" : {
      "title" : "News by Sun, 17 Nov 2019",
      "links" : [
         "https://img.tyt.by/thumbnails/n/buryakina/0e/5/lidiya_ermoshina_20170208_bur_tutby_phsl_-9760.jpg",
         "https://img.tyt.by/thumbnails/n/buryakina/0e/5/lidiya_ermoshina_20170208_bur_tutby_phsl_-9760.jpg"
      ],
      "items" : [
         {
            "link" : "https://news.tut.by/economics/661603.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news",
            "published" : "Sun, 17 Nov 2019 18:03:00 +0300",
            "summary" : "[image 1: Фото: Дарья Бурякина, TUT.BY][1] В воскресенье утром Лукашенко сказал, что ему известны 6 случаев провокаций во время кампании и выборов, и заявил, что что со всеми жестко разберутся.",
            "title" : "Глава ЦИК об инцидентах в избиркомах: Думаю, эти граждане себя точно так же ведут на кухне с женой"
         },
         {
            "link" : "https://news.tut.by/economics/661603.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news",
            "published" : "Sun, 17 Nov 2019 18:03:00 +0300",
            "summary" : "[image 1: Фото: Дарья Бурякина, TUT.BY][1] В воскресенье утром Лукашенко сказал, что ему известны 6 случаев провокаций во время кампании и выборов, и заявил, что что со всеми жестко разберутся.",
            "title" : "Глава ЦИК об инцидентах в избиркомах: Думаю, эти граждане себя точно так же ведут на кухне с женой"
         }
      ]
   },
   "20191116" : {
      "title" : "News by Sat, 16 Nov 2019",
      "links" : [
         "https://img.tyt.by/thumbnails/n/buryakina/08/6/dinamo-torpedo_20191026_bur_tutby_phsl-2466.jpg",
      ],
      "items" : [
         {
            "link" : "https://sport.tut.by/news/hockey/661569.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news",
            "published" : "Sat, 16 Nov 2019 23:02:00 +0300",
            "summary" : "[image 62: Фото: Дарья Бурякина, TUT.BY][62] Главный тренер омского «Авангарда» Боб Хартли недоволен действиями защитника минского «Динамо» Романа Дюкова. Напомним, что после столкновения с Андреем Стасем Дюков долго не мог подняться, после чего судьи удалили игрока «Авангарда» до конца матча.",
            "title" : "«Актеры должны быть в Голливуде, а не на льду!» Тренер «Авангарда» считает хоккеиста «Динамо» симулянтом"
         },
      ]
   }
}
```