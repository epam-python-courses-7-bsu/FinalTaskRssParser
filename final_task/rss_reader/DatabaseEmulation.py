import pickle
from typing import Any
import logging as log
import os
import datetime


now = datetime.datetime.now


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args,
                **kwargs
            )
        return cls._instances[cls]


class DatabaseEmulation(metaclass=Singleton):
    def __init__(self, path_to_dates, path_to_data):
        self.path_to_dates = path_to_dates
        self.path_to_data = path_to_data
        self.dates = {}
        with open(path_to_dates, "r") as data_file:
            for line in data_file:
                date, row_number = line.strip().split()
                self.dates[date] = int(row_number)
        self.dates_file = open(path_to_dates, "a")
        self.write_data_stream = open(self.path_to_data, "ab")
        self.read_data_stream = open(self.path_to_data, "rb")

    def __exit__(self, *args):
        self.dates_file.close()
        self.write_data_stream.close()
        self.read_data_stream.close()

    def check_date(self, date):
        return date in self.dates

    def get_id(self, date):
        return self.dates[date]

    def get_items(self, dump_idx) -> Any:
        for line_id in range(dump_idx):
            pickle.load(self.read_data_stream)
        result = pickle.load(self.read_data_stream)
        self.read_data_stream.seek(0, os.SEEK_SET)
        return result

    def write_items(self, rss_items: dict) -> None:
        idx = len(self.dates)
        date = now().strftime("%d/%m/%Y")
        self.write_data_stream.seek(0, os.SEEK_END)
        pickle.dump(rss_items, self.write_data_stream)
        self.dates[date] = idx
        self.dates_file.write("{} {}\n".format(date, idx))


def get_txt_date(data) -> None:
    date_id = {}
    with open("dates.txt", "r", encoding="utf-8") as f:
        for line in f:
            key, value = line.strip().split()
            date_id[key] = value

    if data == date_id[key]:
        date_id[key] = value
        with open("{}.txt".format(value), "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("There isn't any news from this day")


def cash_news():
    log.info("Try to cash news from stdout")
    data_id = {}
    data = now().strftime("%d/%m/%Y")

    with open("dates.txt", "r", encoding="utf-8") as f:
        for line in f:
            key, *value = line.split()
            data_id[key] = value
    len_txt_date = len(data_id) + 1
    remembered_data = {}
    with open("dates.txt", "w", encoding="utf-8") as f:
        remembered_data[data] = len_txt_date
        f.write(str(remembered_data))
