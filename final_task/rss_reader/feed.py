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
from termcolor import colored



class Feed:
    """Feed class, contain feed info and list of articles """
    def __init__(self, parsed, args):
        """create feed with fixed number of articles """
        logging.info('Started creting feed')

        articles_list = []
        cashed_news_number = 0
        if args.date:
            logging.info('Started extracting data from cache')
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
            logging.info('Finished extracting data from cache')

            if args.limit:
                if args.limit > cashed_news_number and args.date:
                    print(f'Only {cashed_news_number} feeds cashed')
                    number_of_articles = cashed_news_number
                elif not args.date and args.limit > len(parsed.entries):
                    print(f'Only {len(parsed.entries)} feeds cashed')
                    number_of_articles = len(parsed.entries)
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

    def print_readable_feed(self, is_colored):
        """print feed to stdout in readable format"""
        logging.info('Started printing feed')
        print('.' * 79)
        print(f'\n\n{self.feed_name}\n\n')
        print(self.link)
        for article_ in self.articles:
            article_.print_readable_article(is_colored)
        logging.info('Finished printing feed')

    def print_json_feed(self, is_colored):
        """print feed to stdout in json"""
        json = {}
        for i, article_ in enumerate(self.articles):
            name = f"Article {i + 1}"
            json[name] = article_.make_article_json()
        json['Feed'] = self.feed_name
        json['Link'] = self.link
        if is_colored: print('\033[96m')
        pprint(json)
        if is_colored: print('\033[0m')

    def save_feed_to_database(self):
        """
        saving to shelve database instances of article class,
        that curent feed contains
        using article published date as a key
        """
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
        """Creating an html file, using curent datetime as a filename"""
        logging.info('Started saving feed to html file')
        time_now = str(datetime.datetime.now())
        time_for_path = time_now[:-16] + '_' + time_now[-15:-13] + '-' + time_now[-12:-10] + '-' + time_now[-9:-7]
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
                    # if have internet access, downloading images and pasting in a html file
                    for link in article.media:
                        dtags.img(src=link['url'])
                else:
                    # if no, paste links of these images
                    dtags.a('Image links:')
                    for link_number, link in enumerate(article.media):
                        img_url = link['url']
                        dtags.a(f'{link_number + 1}. {img_url}', href=link)
            html += dtags.p(article.summary)
            html += dtags.br()
        with open('html_feeds/' + time_for_path + ' RSS_feeds.html', 'w') as html_file:
            html_file.write(str(html))
        logging.info('Finished saving feed to html file')

    def save_feed_to_pdf(self):
        """Creating an pdf file, using curent datetime as a filename"""
        logging.info('Started saving feed to pdf file')
        time_now = str(datetime.datetime.now())
        time_for_path = time_now[:-16] + '_' + time_now[-15:-13] + '-' + time_now[-12:-10] + '-' + time_now[-9:-7]
        pdf_path = 'pdf_feeds/' + time_for_path + ' RSS_feeds.pdf'
        pdf = FPDF()
        # fonts
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
        pdf.add_font('DejaVu', 'I', 'DejaVuSansCondensed-Oblique.ttf', uni=True)
        pdf.set_font('DejaVu', 'B', 25)

        pdf.add_page()
        pdf.set_text_color(0,0,228)
        # feed source
        pdf.cell(0, 0, f'Feeds from {self.link}', 0, 1,align='C', link = self.link)
        pdf.set_text_color(0,0,0)
        pdf.set_font('DejaVu', '', 14)
        # list of articles that current feed contains (clickable)
        for article_number, article in enumerate(self.articles):
            pdf.write(5,'\n\n' + str(article_number + 1) + '. ' + article.title, link=article.link)
        # articles
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
                # if have internet access, downloading images and pasting in a pdf file
                for img_number, img in enumerate(article.media):
                    img_url = img['url']
                    if img_url != '':
                        image = r.get(img_url)
                        img_path = str(article_number + 1) + '_' + str(img_number + 1) + '_img.jpg'
                        with open(img_path, 'wb') as file:
                            file.write(image.content)
                        try:
                            pdf.image(img_path,w = 50, h = 50)
                        except (SyntaxError, RuntimeError):
                            pdf.write(15, 'Media link(clickable)' + '\n\n', link=img['url'])
                        os.remove(img_path)
            else:
                # if no, paste links of these images (clickable)
                pdf.write(15, "Image links (clickable):\n")
                for img_number, img in enumerate(article.media):
                    pdf.write(15,str(img_number + 1) + '. ' + article.media_description, link=img['url'])
                    pdf.write(15,str(img_number + 1) + '.\n', link=img['url'])
            pdf.write(10, article.summary)
        pdf.output(pdf_path)
        logging.info('Finished saving feed to pdf file')

        
