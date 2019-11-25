import weasyprint
import logging
import pkg_resources

from jinja2 import Environment, FileSystemLoader

from exceptions import NoDataToConvertError


STATIC_PATH = pkg_resources.resource_filename('rss_reader', 'static/')


def converter(news_articles, path_to_html, path_to_pdf):
    """entry point for format conversion"""
    articles_in_html = convert_to_html(news_articles)
    if path_to_html:
        logging.info('Converting to html')
        save_html(articles_in_html, path_to_html)
    if path_to_pdf:
        logging.info('Converting to pdf')
        save_pdf(articles_in_html, path_to_pdf)


def convert_to_html(news_articles):
    """convert news_articles to HTML"""
    file_loader = FileSystemLoader(f'{STATIC_PATH}')
    env = Environment(loader=file_loader)
    template = env.get_template('template.html')
    if news_articles:
        output = template.render(news_articles=news_articles)
        return output
    else:
        raise NoDataToConvertError()


def save_html(articles_in_html, path):
    """save rendered html to html file"""
    with open(f'{path}.html', 'w') as file:
        file.writelines(articles_in_html)
        print(f'Convertion to html is complete. File {path}.html is created')


def save_pdf(articles_in_html, path):
    """save rendered html code to pdf file"""
    weasyprint.HTML(string=articles_in_html).write_pdf(f'{path}.pdf')
    print(f'Convertion to pdf is complete. File {path}.pdf is created')
