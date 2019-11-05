from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name="rss-reader",
    version='3.5',
    packages=find_packages(),
    author="Vlad Protosevich",
    author_email="protosevic2001@gmail.com",
    install_requires=['feedparser==5.2.1'],
    entry_points={
        'console_scripts': [
            'rss-reader = rss_reader.rss_reader:run'
        ]
    },
)