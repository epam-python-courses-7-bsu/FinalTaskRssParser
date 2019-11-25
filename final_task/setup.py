from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='rss-reader',
    version='1.0',
    packages=find_packages(),
    py_modules=['rss_reader.py'],
    install_requires = ['feedparser', 'bs4'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author="Oleg Slavashevich",
    author_email="oslavashevish@gmail.com",
    entry_points = {
        'console_scripts': [
            'rss_reader = rss_reader.rss_reader:main'
        ]
    }
)