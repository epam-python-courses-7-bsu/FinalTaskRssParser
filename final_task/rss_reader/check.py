import urllib.error
import urllib.request


def internet_on():
    try:
        urllib.request.urlopen("http://google.com", timeout=5)
        return True
    except (urllib.error.URLError, urllib.error.HTTPError):
        return False
