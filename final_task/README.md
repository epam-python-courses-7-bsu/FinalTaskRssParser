This rss-reader uses requests library to get requests from news websites.
BeautifulSoup from bs4 library enables to find all "items" (pieces of news) from rss feed.
The components of news are devided into groups (title, description, image, link) using dictionary.
News are converted into JSON format using json library method "dumps".  
Example of JSON format: 
{
"title": "Lebanese banks urge calm amid financial crisis, protests",
"date": "Sat, 09 Nov 2019 13:20:48 -0500",
"description": "The country's financial troubles have worsened since nationwide protests — initially against new taxes — snowballed into calls for the entire political elite to step down.  Banks reopened Nov. 1 after a two-week closure amid the protests.  The announcement by Salim Sfeir, chairman of the Association of Banks in Lebanon, came after a two-hour meeting between President Michel Aoun, several Cabinet ministers and top banking officials in search of solutions for Lebanon's deepening financial and economic crisis.",
"link": "https://news.yahoo.com/lebanons-president-meets-bankers-amid-151829256.html",
"image": "http://l.yimg.com/uu/api/res/1.2/vV6YKXA7Yw.7FkwDMVwC1g--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/ap.org/bfc75d01189b241cdb49d85b07c1122f",
"alt": "Lebanese banks urge calm amid financial crisis, protests"
}
Convertion:
Dominate lib is used to create html files.
FPDF lib is used to create pdf files.
When loading images for pdf, caching is used to fasten loading(httplib2)
