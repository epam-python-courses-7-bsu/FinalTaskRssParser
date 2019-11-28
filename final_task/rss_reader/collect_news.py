import feedparser
import html

from . import logg, converter, news_parser


def collectNews(limit, tojson, tohtml, topdf, color, source):
    '''
    1. cache news
    2. create html or pdf document
    3. or return news in json or normal format
    '''
    news = list()

    channel = feedparser.parse(source)
    news.append(color[0] + "Feed: " + channel.feed.title + '\n')
    limit = limit or len(channel.entries)

    news_parser.cacheNews(channel)

    if (tohtml or topdf):
        html_doc = converter.createHtmlStructure(channel, limit, tohtml, topdf)
        return html_doc
    else:
        for index, item in enumerate(channel.entries):
            if (index == limit):
                break

            if(index%2==0):
                news.append(color[1])
            else:
                news.append(color[2])

            logg.createLogs(item)

            if (tojson):
                news.append(news_parser.intoJson(item))
            else:
                news.append("\nTitle: " + html.unescape(item.title))
                news.append("\nDate: " + item.published)
                news.append("\nLink: " + item.link + '\n')
                description = news_parser.getDescription(item.description)
                if(description):
                    news.append(color[0] + "Description: " + description + '\n')
                news.append(color[1] + "Links:" + "\n[1]: " + item.link + "(link)")
                media_content = news_parser.checkMediaContent(item)
                if(media_content):
                    news.append("\n[2]: " + media_content + '\n')

        return news

