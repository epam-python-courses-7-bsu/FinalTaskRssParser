"""Module contain definition of "News" class"""

from dataclasses import dataclass
from termcolor import cprint
import argparse

@dataclass
class News:
    """Class that represent single entry of news

    Uses for storing title, date, link, text, links from text, source and feed_title as an attributes of class.
    Class have attribute "command_line_args", that passes inside functions.process_func.process_feed() function and is
    instance of argparse.Namespace.
    """
    title: str
    date: str
    link: str
    text: str
    links: str
    feed_title: str
    source: str


    def create_list_of_links(self):
        """Turn tuple ([href_links], [img_links]) into list of links"""
        # Merge list of links
        list_of_links = self.links[0] + self.links[1]
        return list_of_links


    def create_string_of_links(self):
        """Turn tuple ([href_links], [img_links]) of lists into formatted string"""
        # Merge list of links
        list_of_links = self.create_list_of_links()

        string_repr_of_links = ''
        for num, link in enumerate(list_of_links):
            if link:
                string_repr_of_links = string_repr_of_links + f"[{num+1}] {link}\n"
        return string_repr_of_links


    def print_feed_title(self):
        """Print feed title"""
        if self.command_line_args.colorize:
            cprint(self.feed_title, 'magenta')
        else:
            print(self.feed_title)


    def print_news(self):
        """Print to stdout title, date, link, text
        and links from text in particular sequence."""
        if self.command_line_args.colorize:
            list_of_colors = ['magenta', 'green', 'blue']
        else:
            list_of_colors = ['white', 'white', 'white']
        cprint('-----------------------------------------------------------', list_of_colors[0])
        cprint('Title: '+self.title, list_of_colors[0])
        cprint('Date: '+self.date, list_of_colors[0])
        cprint('Link: '+self.link, list_of_colors[0], end='\n\n')
        cprint(self.text, list_of_colors[1], end='\n\n')
        links = self.create_string_of_links()
        if links:
            cprint('Links:', list_of_colors[2])
            cprint(links, list_of_colors[2])
        cprint('-----------------------------------------------------------', list_of_colors[0])
