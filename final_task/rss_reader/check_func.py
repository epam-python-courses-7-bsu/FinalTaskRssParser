import requests
import exceptions as ex


def internet_connection_check():
    url = 'http://www.google.com/'
    timeout = 5
    is_internet = True
    try:
        requests.get(url, timeout=timeout)
    except requests.ConnectionError:
        is_internet = False
    finally:
        return is_internet
