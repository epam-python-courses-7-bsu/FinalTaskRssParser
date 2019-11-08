from setuptools import setup, find_packages
from os.path import join, dirname
import rss_reader

setup(
    name="rss-reader",
    version=rss_reader.VERSION,
    packages=['rss_reader'],
    author="Vlad Protosevich",
    author_email="protosevic2001@gmail.com",
    install_requires=['feedparser==5.2.1'],
    entry_points={
        'console_scripts': [
            'rss-reader = rss_reader.rss_reader:run'
        ]
    },
)