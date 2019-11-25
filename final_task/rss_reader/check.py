import requests


def internet_on():
    """ Check internet connection function. """
    try:
        requests.get("http://google.com", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        print("Please, check your internet connection.")
