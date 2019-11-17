from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rss-reader',
    version='3.0',
    description='Pure Python command-line RSS reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Kirill-Ulich/FinalTaskRssParser/tree/master/final_task',
    author='Kirill Ulich',
    author_email='k.ulitch@yandex.ru',
    license='MIT',
    zip_safe=False,
    scripts=['rss_reader/exceptions.py',
             'rss_reader/items.py',
             'rss_reader/log.py',
             'rss_reader/news_converter.py',
             'rss_reader/news_storage.py',
             'rss_reader/parser_rss.py',
             'rss_reader/rss_reader.py',
             'rss_reader/tools.py'],
    install_requires=['feedparser==5.2.1', 'bs4==0.0.1'],
    entry_points={
        'console_scripts': ['rss-reader=rss_reader:main'],
    }
)
