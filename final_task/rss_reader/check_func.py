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


def check_data_base(path):
    with shelve.open(path) as database:
        if not database:
            raise ex.EmptyDataBase('Local feed storage is empty')


def is_date_in_database(date, path):
    with shelve.open(path) as database:
        if date not in database:
            raise ex.DateNotInDatabase('There is no feeds with this date and source in local storage')