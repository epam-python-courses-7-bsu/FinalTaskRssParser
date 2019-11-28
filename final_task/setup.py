from setuptools import setup, find_packages
import os
from rss_reader import version


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name="rss_reader",
    version=version.VERSION,
    packages=find_packages(),
    install_requires=['argparse','beautifulsoup4','dominate','feedparser', 'urllib3', 'xhtml2pdf', 'colored', 'requests', 'psycopg2','flask'],
    author="ilya khonenko",
    author_email="honenkoi@gmail.com",
    url="https://github.com/kingofmidas",
    description="This is rss-reader",
    long_description = long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="rss reader",
    python_requires='>=3.8',
)
