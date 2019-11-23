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
<<<<<<< HEAD
from termcolor import colored
=======
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762



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

<<<<<<< HEAD
    def print_readable_feed(self, is_colored):
=======
    def print_readable_feed(self):
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762
        """print feed to stdout in readable format"""
        logging.info('Started printing feed')
        print('.' * 79)
        print(f'\n\n{self.feed_name}\n\n')
        print(self.link)
        for article_ in self.articles:
<<<<<<< HEAD
            article_.print_readable_article(is_colored)
        logging.info('Finished printing feed')

    def print_json_feed(self, is_colored):
=======
            article_.print_readable_article()
        logging.info('Finished printing feed')

    def print_json_feed(self):
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762
        """print feed to stdout in json"""
        json = {}
        for i, article_ in enumerate(self.articles):
            name = f"Article {i + 1}"
            json[name] = article_.make_article_json()
        json['Feed'] = self.feed_name
        json['Link'] = self.link
<<<<<<< HEAD
        if is_colored: print('\033[96m')
        pprint(json)
        if is_colored: print('\033[0m')
=======
        pprint(json)
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762

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
<<<<<<< HEAD
        time_now = str(datetime.datetime.now())
        time_for_path = time_now[:-16] + '_' + time_now[-15:-13] + '-' + time_now[-12:-10] + '-' + time_now[-9:-7]
=======
        todays_date = str(datetime.datetime.now())[:-7] + ' '
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762
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
<<<<<<< HEAD
        with open('html_feeds/' + time_for_path + ' RSS_feeds.html', 'w') as html_file:
            html_file.write(str(html))
=======
        with open('html_feeds/' + todays_date + ' RSS_feeds.html', 'w') as html_file:
            html_file.write(str(html))
        return html
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762

    def save_feed_to_pdf(self):
        time_now = str(datetime.datetime.now())
        time_for_path = time_now[:-16] + '_' + time_now[-15:-13] + '-' + time_now[-12:-10] + '-' + time_now[-9:-7]
        pdf_path = 'pdf_feeds/' + time_for_path + ' RSS_feeds.pdf'
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
            pdf.write(5,'\n\n' + str(article_number + 1) + '. ' + article.title, link=article.link)
        for article_number, article in enumerate(self.articles):
            pdf.add_page()
            pdf.set_font('DejaVu', 'B', 18)
            pdf.write(5,'\n' + str(article_number + 1) + '. ' + article.title + '\n', link=article.link)
            pdf.set_font('DejaVu', 'I', 18)
            date = article.published
            str_date = f'{date.tm_year}/{date.tm_mon}/{date.tm_mday} {date.tm_hour}:{date.tm_min}'
            pdf.write(5,'\n' + str_date + '\n\n\n')
            pdf.set_font('DejaVu','',12)
            if check.internet_connection_check():
                for img_number, img in enumerate(article.media):
                    img_url = img['url']
                    if img_url != '':
                        image = r.get(img_url)
                        img_path = str(article_number + 1) + '_' + str(img_number + 1) + '_img.jpg'
<<<<<<< HEAD
=======
                        print(img_path)
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762
                        with open(img_path, 'wb') as file:
                            file.write(image.content)
                        try:
                            pdf.image(img_path,w = 50, h = 50)
                        except (SyntaxError, RuntimeError):
<<<<<<< HEAD
                            pdf.write(15, 'Media link(clickable)' + '\n\n', link=img['url'])
=======
                            pdf.write(15, img['url'], link=img['url'])
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762
                        os.remove(img_path)
            else:
                pdf.write(15, "Image links (clickable):\n")
                for img_number, img in enumerate(article.media):
<<<<<<< HEAD
                    pdf.write(15,str(img_number + 1) + '. ' + article.media_description, link=img['url'])
=======
                    pdf.write(15,str(img_number + 1) + '.\n', link=img['url'])
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762

            pdf.write(10, article.summary)

        pdf.output(pdf_path)

        
