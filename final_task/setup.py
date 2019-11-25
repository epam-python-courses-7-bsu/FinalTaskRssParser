from setuptools import setup, find_packages
import os

setup(name='Rss reader',
      version='1.4.3',
      description='Pure Python command-line RSS reader.',
      author='Marina Romanchuk',
      author_email='marina-romanchuk-2015@mail.ru',
      data_files=[('rss_reader', ['rss_reader/ARIALUNI.ttf'])],
      install_requires=['feedparser', 'doc', 'yattag', 'requests', 'fpdf'],
      include_package_data=True,
      zip_safe=False,
      packages=find_packages(),
      scripts=['rss_reader/rss_parser.py',
               'rss_reader/console_interface.py',
               'rss_reader/database_functions.py',
               'rss_reader/rss_reader.py',
               'rss_reader/conversion_functions.py',
               'rss_reader/information_about_news.py'],
      entry_points={'console_scripts': ['rss-reader=rss_reader:main']}
)