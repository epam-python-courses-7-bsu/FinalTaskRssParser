from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rss-reader',
    version='2.0',
    description='Pure Python command-line RSS reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Kirill-Ulich/FinalTaskRssParser/tree/master/final_task',
    author='Kirill Ulich',
    author_email='k.ulitch@yandex.ru',
    license='MIT',
    packages=find_packages(exclude=['rss_reader', 'tests']),
    zip_safe=False,
    install_requires=['feedparser', 'bs4']
)
