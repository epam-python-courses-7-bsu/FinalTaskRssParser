import csv
from datetime import date
from dateutil.parser import parse
from dataclasses import dataclass, asdict

import ClassNews

FIELDNAMES = ['date', 'title', 'link', 'article', 'links']


def csv_to_python(articles_list, csv_file):
    """This function inserts news to the source csv file that has never been seen in it."""
    articles_list_from_csv = []
    with open(csv_file, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file, FIELDNAMES, delimiter='\t')
        for item in reader:
            r = ClassNews.Article(item['title'], item['date'], item['link'], item['article'], item['links'])
            articles_list_from_csv.append(r)

    union_list = articles_list_from_csv[:]
    for item in articles_list:
        if item not in articles_list_from_csv:
            union_list.append(item)

    with open(csv_file, "w",encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, delimiter='\t')
        for item in union_list:
            writer.writerow(asdict(item))


def return_news_to_date(input_date, csv_file, limit):
    """This function read from the file those news that match by date"""
    article_list_by_date = []
    datetime_input = date(int(input_date[0:4]), int(input_date[4:6]), int(input_date[6:8]))
    with open(csv_file, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file, FIELDNAMES, delimiter='\t')
        match_counter = 0
        for item in reader:
            article_from_file = ClassNews.Article(item['title'], item['date'], item['link'], item['article'], item['links'])

            date_time = parse(article_from_file.date)
            date_from_file = date_time.date()

            if date_from_file == datetime_input:
                match_counter += 1
                article_list_by_date.append(article_from_file)

            if limit == match_counter:
                return article_list_by_date

    return article_list_by_date