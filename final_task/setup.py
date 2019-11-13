from setuptools import setup, find_packages
from rss_reader/rss_reader import VERSION

setup(
    name='rss_reader',
    version=VERSION,
    packages=find_packages(),
    install_requires=['feedparser', 'bs4'],
    author="Victoria Kondrat'eva",
    author_email='sam.kondrateva@gmail.com',
    url='https://github.com/Victoria-Sam',
    description='RSS Reader',
    entry_points={'console_scripts': ['Rss-Reader = rss_reader.rss_reader:main']},
    keywords="rss reader",
    python_requires = '>=3.7',
)