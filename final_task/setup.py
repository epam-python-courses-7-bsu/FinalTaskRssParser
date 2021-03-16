from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name="rss-reader",
    version="2.2",
    packages=['rss_reader'],
    zip_safe=True,
    scripts=['rss_reader/rss_reader.py', 'rss_reader/json_date_util.py', 'rss_reader/text_work_util.py'],

    install_requires=['feedparser==5.2.1'],

    author="Oleg Mikus",
    author_email="mikus.oleg@gmail.com",

    entry_points={
        'console_scripts': [
            'rss-reader = rss_reader:main_func'
        ]
    },

)