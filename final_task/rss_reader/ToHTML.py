from jinja2 import Environment, FileSystemLoader
import os

FILENAME_HTML = "articles.html"


def print_article_list_to_html(list_articles, path):
    if not os.path.exists(path):
        raise FileNotFoundError
    html_stream = print_article_list(list_articles)
    with open(os.path.join(path, FILENAME_HTML), "w", encoding='utf-8') as html:
        html.write(html_stream)


def print_article_list(list_articles):
    # directory with templates
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    return template.render(articles=list_articles)