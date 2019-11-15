from dataclasses import dataclass
from string_operations import cut_string_to_length_with_space

@dataclass
class Article:
    title: str
    link: str
    date: str
    summary: str
    media: str
    media_description: str

    def print_readable_article(self):
        print("_" * 79)
        print(self.date[:-6], ':\n')
        cutted_title = cut_string_to_length_with_space(self.title, 77)
        for i, string in enumerate(cutted_title):
            if i + 1 == len(cutted_title):
                print(string, [1])
            else:
                print(string)

        str_number_of_img = ' '
        if len(self.media) > 1:
            str_number_of_img = ' - [{}]'.format(len(self.media) + 1)
        print('\n\nImages:\n{} [2]{}\n'.format(self.media_description, str_number_of_img))
        cutted_summary = cut_string_to_length_with_space(self.summary, 79)
        for string in cutted_summary:
            print(string)
        print('\n\nLinks:\n[1]', self.link)
        for i, img in enumerate(self.media):
            print('[{}]'.format(i+2), img['url'])
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
