import csv

def addcsv(articles):
    with open('news.csv', 'a', newline='') as csvfile:
        fieldnames = ['link','title', 'img', 'summary', 'published']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow(articles)

def out():
    a = []
    with open('news.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            a.append(row)
    return a