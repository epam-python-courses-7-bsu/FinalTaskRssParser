"""Module converts articles to html file"""
import os
from typing import Optional

from argparse_handler import check_the_connection
import datetime
import urllib.request

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

directory_to_module = os.path.abspath(os.path.dirname(__file__))


def convert_to_html(articles_list: list, path: str, rss_url: Optional[str]) -> None:
    """Converts articles to html format"""
    templates_path = os.path.join(directory_to_module, 'templates')
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template('base.html')

    css_file_path = os.path.join(templates_path, 'style.css')

    connection_info = check_the_connection('https://www.google.com/')
    connection = connection_info == 'ok'

    today = datetime.date.today().strftime("%B %d, %Y")
    if rss_url:
        source = urllib.request.urlparse(rss_url).hostname
        filename = f'{today} {source}.html'
        title = f'News file created: {today}, Source: {source}'
    else:
        filename = f'{today}.html'
        title = f'News file created: {today}'
    full_name = os.path.join(path, filename)

    html = template.render(articles_list=articles_list,
                           connection=connection,
                           css_path=css_file_path,
                           title=title)

    soup = BeautifulSoup(html, features="html.parser")
    pretty_html = soup.prettify()

    try:
        with open(full_name, 'w', encoding="utf-8") as the_file:
            the_file.write(pretty_html)
    except PermissionError:
        print('You need to run program as system administrator, to save files in that location')

