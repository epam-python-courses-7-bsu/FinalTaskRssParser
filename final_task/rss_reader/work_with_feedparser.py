import decorators
import RssReaderException
import feedparser
import os


@decorators.functions_log
def get_object_feed(url: str) -> feedparser.FeedParserDict:
    try:
        data = feedparser.parse(url)
        try:
            if data.status == 200:
                if data['version']:
                    return data
                else:
                    raise RssReaderException.ConnectException(f'There is no rss feed at this url: {url}')
            else:
                raise RssReaderException.ConnectException(f'HTTP Status Code {data.status}')
        except AttributeError:
            if os.path.isfile(url):
                if data['version']:
                    return data
                else:
                    raise RssReaderException.ConnectException(f'There is no rss feed at this url: {url}')
            else:
                raise RssReaderException.ConnectException(f'HTTP Status Code {data.status}')
    except AttributeError:
        raise RssReaderException.ConnectException(f'{url} - is not url(example url "https://google.com")')
    except Exception as exc:
        raise RssReaderException.ConnectException(exc)