import sys
sys.path.append('rss_reader')
from setuptools import setup, find_packages
from rss_reader import rss_reader

setup(
    name='rss_reader',
    version=rss_reader.VERSION,
    packages=find_packages(),
    install_requires=['feedparser', 'bs4', 'unidecode', 'fpdf', 'ebooklib', 'colored'],
    author="Victoria Kondrat'eva",
    author_email='sam.kondrateva@gmail.com',
    url='https://github.com/Victoria-Sam',
    description='RSS Reader',
    entry_points={'console_scripts': ['Rss-Reader = rss_reader.rss_reader:main']},
    keywords="rss-reader",
    python_requires='>=3.7',
)
