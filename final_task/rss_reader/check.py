import urllib.error
import urllib.request


def internet_on():
    try:
        urllib.error.urlopen('http://216.58.192.142', timeout=5)
        return True
    except urllib.request.URLError as err:
        return False
