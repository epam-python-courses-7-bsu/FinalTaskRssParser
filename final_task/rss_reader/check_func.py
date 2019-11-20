import requests
import exceptions as ex
import shelve


def internet_connection_check():
    url='http://www.google.com/'
    timeout=5
    try:
        requests.get(url, timeout = timeout)
    except requests.ConnectionError:
        raise ex.NoInternetConnection("No internet connection")
