from string_operations import *
import logging
import datetime
from termcolor import colored



class Article:
    """single article class"""

    def __init__(self, parsed, source):
        """receive parsed article and extracts data from it"""
        self.title = make_string_readable(parsed.title)
        self.link = parsed.link
        self.feed_link = source
        self.published = extract_date(parsed)
        summary_ = extract_topic_info_from_summary(parsed.summary)
        self.summary = make_string_readable(summary_)
        self.media = parsed.media_content

        description_ = extract_image_info_from_summary(parsed.summary)
        self.media_description = make_string_readable(description_)

    def print_readable_article(self, is_colored):
        """print article to stdout in human-readable format"""
        print( "_" * 79)
        date = self.published
        date_for_print = f'{date.tm_year}/{date.tm_mon}/{date.tm_mday}, {date.tm_hour}:{date.tm_min}:{date.tm_sec}\n'
        if is_colored:
            print(colored(date_for_print, 'red'))
        else:
            print(date_for_print)

        cutted_title = cut_string_to_length_with_space(self.title, 77)
        for str_number, string in enumerate(cutted_title):
            if str_number + 1 == len(cutted_title):
                if is_colored:
                    print(colored(string + '[1]', 'red'))
                else:
                    print(string + '[1]')
            else:
                if is_colored:
                    print(colored(string, 'red'))
                else:
                    print(string)

        # images description and their links numbers (like [2] - [5])
        str_number_of_img = ' '
        if len(self.media) > 1:
            str_number_of_img = f' - [{len(self.media) + 1}]'
        images_and_link_numbers = f'\n\nImages:\n{self.media_description} [2] - {str_number_of_img}\n'
        if is_colored:
            print(colored(images_and_link_numbers, 'blue'))
        else:
            print(images_and_link_numbers)
        

        cutted_summary = cut_string_to_length_with_space(self.summary, 79)
        for string in cutted_summary:
            if is_colored:
                print(colored(string, 'cyan'))
            else:
                print(string)

        # Links of article and images
        if is_colored:
            print(colored('\n\nLinks:\n[1]' + self.link, 'green'))
        else:
            print('\n\nLinks:\n[1]', self.link)
        for number, img in enumerate(self.media):
            if is_colored:
                print(colored(f'[{number+2}] ' + img['url'], 'green'))
            else:
                print(f'[{number+2}]', img['url'])

        print("_" * 79)

    def make_article_json(self):
        """convert article data in json format"""
        json = {
            'images': {self.media_description: img['url'] for img in self.media},
            'link': self.link,
            'summary': self.summary,
            'date': self.published,
            'title': self.title,
        }
        return json
