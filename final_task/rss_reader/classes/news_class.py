"""Module contain definition of "News" class"""

from dataclasses import dataclass

@dataclass
class News:
    """Class that represent single entry of news

    Uses for storing title, date, link, text and links from text
    as an attributes of class.
    """
    title: str
    date: str
    link: str
    text: str
    links: str
    feed_title: str
    source: str


    def print_feed_title(self):
        """Print feed title"""
        print(self.feed_title)

    def create_list_of_links(self):
        """Turn tuple ([href_links], [img_links]) into list of links"""
        # Merge list of links
        list_of_links = []
        list_of_links.extend(self.links[0])
        list_of_links.extend(self.links[1])
        return list_of_links

    def create_string_of_links(self):
        """Turn tuple ([href_links], [img_links]) of lists into formatted string"""
        # Merge list of links
        list_of_links = self.create_list_of_links()

        string_repr_of_links = ''
        for num, link in enumerate(list_of_links):
            if link:
                string_repr_of_links = string_repr_of_links + '[{}] '.format(num + 1) + link + '\n'
        self.links = string_repr_of_links


    def print_news(self):
        """Print to stdout title, date, link, text
        and links from text in particular sequence."""
        print('-----------------------------------------------------------')
        print('Title: '+self.title)
        print('Date: '+self.date)
        print('Link: '+self.link, end='\n\n')
        print(self.text, end='\n\n')
        if self.links:
            print('Links:')
            print(self.links)
        print('-----------------------------------------------------------')
