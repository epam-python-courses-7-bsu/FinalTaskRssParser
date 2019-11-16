from string_operations import *
import logging


class Article:
    """single article class"""

    def __init__(self, parsed):
        """receive parsed article and extracts data from it"""
        logging.info('      title')
        self.title = make_string_readable(parsed.title)

        logging.info('      link')
        self.link = parsed.link

        logging.info('      date')
        self.published = extract_date(parsed)

        logging.info('      summary')
        summary_ = extract_topic_info_from_summary(parsed.summary)
        self.summary = make_string_readable(summary_)

        logging.info('      image links')
        self.media = parsed.media_content

        logging.info('      image description')
        description_ = extract_image_info_from_summary(parsed.summary)
        self.media_description = make_string_readable(description_)

    def print_readable_article(self):
        """print article to stdout in human-readable format"""

        # separation line
        print("_" * 79)

        # date
        print(self.published[:-6], ':\n')

        # title
        cutted_title = cut_string_to_length_with_space(self.title, 77)
        for i, string in enumerate(cutted_title):
            if i + 1 == len(cutted_title):
                print(string, [1])
            else:
                print(string)

        # images description and their links numbers (like [2] - [5])
        str_number_of_img = ' '
        if len(self.media) > 1:
            str_number_of_img = ' - [{}]'.format(len(self.media) + 1)
        print('\n\nImages:\n{} [2]{}\n'.format(self.media_description, str_number_of_img))

        # topic summary
        cutted_summary = cut_string_to_length_with_space(self.summary, 79)
        for string in cutted_summary:
            print(string)

        # Links of article and images
        print('\n\nLinks:\n[1]', self.link)
        for i, img in enumerate(self.media):
            print('[{}]'.format(i+2), img['url'])

        # separation lane
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
