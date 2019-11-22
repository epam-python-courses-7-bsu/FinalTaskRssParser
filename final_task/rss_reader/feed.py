import logging
import requests as r
import os
from string_operations import make_string_readable
import exceptions as ex
from pprint import pprint
import article
import shelve
import check_func as check
import datetime
import dominate
import dominate.tags as dtags
from fpdf import FPDF



class Feed:
    """Feed class, contain feed info and list of articles """
    def __init__(self, parsed, args):
        """create feed with fixed number of articles """
        logging.info('Started creting feed')

        articles_list = []
        cashed_news_number = 0
        if args.date:
            logging.info('Started extracting data from cash')
            self.link = args.source
            self.feed_name = f'Feeds from {args.source}'
            with shelve.open('cashed_feeds') as database:
                if not database:
                    raise ex.EmptyDataBase('Local feed storage is empty')
                for date in database:
                    if args.date in date and database[date].feed_link == args.source:
                        articles_list.append(database[date])
                        cashed_news_number += 1
            if cashed_news_number == 0:
                raise ex.DateNotInDatabase('There is no feeds with this date and source in local storage')

            if args.limit:
                if args.limit > cashed_news_number:
                    print(f'Only {cashed_news_number} feeds cashed')
                    number_of_articles = cashed_news_number
                else:
                    number_of_articles = args.limit
                articles_list = articles_list[:number_of_articles]
        else:
            if args.limit:
                if args.limit > len(parsed.entries):
                    print(f'Only {len(parsed.entries)} feeds avaliable')
                    number_of_articles = len(parsed.entries)
                else:
                    number_of_articles = args.limit
            else:
                number_of_articles = len(parsed.entries)
            for i in range(number_of_articles):
                articles_list.append(article.Article(parsed.entries[i], args.source))

            self.feed_name = make_string_readable(parsed.feed.title)
            self.link = parsed.feed.link
        self.articles = articles_list

    def print_readable_feed(self):
        """print feed to stdout in readable format"""
        logging.info('Started printing feed')
        print('.' * 79)
        print(f'\n\n{self.feed_name}\n\n')
        print(self.link)
        for article_ in self.articles:
            article_.print_readable_article()
        logging.info('Finished printing feed')

    def print_json_feed(self):
        """print feed to stdout in json"""
        json = {}
        for i, article_ in enumerate(self.articles):
            name = f"Article {i + 1}"
            json[name] = article_.make_article_json()
        json['Feed'] = self.feed_name
        json['Link'] = self.link
        pprint(json)

    def save_feed_to_database(self):
        logging.info('Saving feed to database')
        with shelve.open('cashed_feeds') as database:
            for article in self.articles:
                year = article.published.tm_year
                mon = article.published.tm_mon
                day = article.published.tm_mday
                hour = article.published.tm_hour
                minute = article.published.tm_min
                sec = article.published.tm_sec
                date = f'{year}{mon}{day} {hour}:{minute}:{sec}'
                if date not in database:
                    database[date] = article
        logging.info('feed saved')

    def save_feed_to_html(self):
        todays_date = str(datetime.datetime.now())[:-7] + ' '
        html = dominate.document(title="HTML RSS feed")
        with html.head:
            dtags.meta(charset='utf-8')
        html += dtags.h1(self.feed_name)
        for article_number, article in enumerate(self.articles):
            html += dtags.br()

            date = article.published
            str_date = f'{date.tm_year}/{date.tm_mon}/{date.tm_mday} {date.tm_hour}:{date.tm_min}'

            html += dtags.h2(f'{article_number + 1}.  {article.title}')
            html += dtags.h3(f'   {str_date}')

            html += dtags.a(f'Link: {article.link}')
            html += dtags.br()

            with html:
                if check.internet_connection_check():
                    for link in article.media:
                        dtags.img(src=link['url'])
                else:
                    dtags.a('Image links:')
                    for link_number, link in enumerate(article.media):
                        img_url = link['url']
                        dtags.a(f'{link_number + 1}. {img_url}', href=link)
            html += dtags.p(article.summary)
            html += dtags.br()
        with open('html_feeds/' + todays_date + ' RSS_feeds.html', 'w') as html_file:
            html_file.write(str(html))
        return html

    def save_feed_to_pdf(self):
        todays_date = str(datetime.datetime.now())[:-7] + ' '
        pdf_path = 'pdf_feeds/' + todays_date + ' RSS_feeds.pdf'
        pdf = FPDF()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
        pdf.add_font('DejaVu', 'I', 'DejaVuSansCondensed-Oblique.ttf', uni=True)
        pdf.set_font('DejaVu', 'B', 25)
        pdf.add_page()
        pdf.set_text_color(0,0,228)
        pdf.cell(0, 0, f'Feeds from {self.link}', 0, 1,align='C', link = self.link)
        pdf.set_text_color(0,0,0)
        pdf.set_font('DejaVu', '', 14)
        for article_number, article in enumerate(self.articles):
            pdf.write(5,'\n\n' + str(article_number + 1) + '. ' + article.title)
        for article_number, article in enumerate(self.articles):
            pdf.add_page()
            pdf.set_font('DejaVu', 'B', 18)
            pdf.write(5,'\n' + article.title + '\n', link=article.link)
            pdf.set_font('DejaVu', 'I', 18)
            date = article.published
            str_date = f'{date.tm_year}/{date.tm_mon}/{date.tm_mday} {date.tm_hour}:{date.tm_min}'
            pdf.write(5,'\n' + str_date + '\n\n\n')
            pdf.set_font('Times','',12)
            if check.internet_connection_check():
                for img_number, img in enumerate(article.media):
                    img_url = img['url']
                    if img_url != '':
                        image = r.get(img_url)
                        img_path = str(img_number+ 1) + '_' + str(article_number) + '_img.' + str(img_url[-3:])
                        try:   
                            with open(img_path, 'wb') as file:
                                file.write(image.content)
                            pdf.image(img_path,w = 50, h = 50)
                        except RuntimeError:
                            os.remove(img_path)
                            img_path = str(img_number+ 1) + '_' + str(article_number) + '_img.jpg'
                            with open(img_path, 'wb') as file:
                                file.write(image.content)
                            pdf.image(img_path,w = 50, h = 50)

                        os.remove(img_path)
            else:
                pdf.write(15, "Image links (clickable):\n")
                for img_number, img in enumerate(article.media):
                    pdf.write(15,str(img_number + 1) + '.\n', link=img['url'])

            pdf.write(10, article.summary)

        pdf.output(pdf_path)

        
