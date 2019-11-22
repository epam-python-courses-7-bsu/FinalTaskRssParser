from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rss-reader',
    version='5.0',
    description='Pure Python command-line RSS reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/paxalos/FinalTaskRssParser/tree/master/final_task',
    author='Pavel Los',
    author_email='Lospawel@yandex.ru',
    license='MIT',
    zip_safe=False,
    scripts=['rss_reader/custom_exceptions.py',
             'rss_reader/database_functions.py',
             'rss_reader/parse_rss_functions.py',
             'rss_reader/print_functions.py',
             'rss_reader/rss_reader.py',
             'rss_reader/save_in_format_functions.py',
             'rss_reader/arguments_functions.py'],
    install_requires=['feedparser',
                      'termcolor',
                      'pymysql',
                      'colorama',
                      'mysql-connector-python',
                      'py-dateutil',
                      'requests'],
    entry_points={
        'console_scripts': ['rss-reader=rss_reader:main'],
    }
)