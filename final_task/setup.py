import os
from setuptools import setup, find_packages


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as foo:
    long_description = foo.read()


setup(
    name="rss_reader",
    version="4.0",
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'feedparser', 'urllib.error'],
    author="Stacy Merkushova",
    author_email="st.merkush@gmail.com",
    url="https://github.com/Clonder/FinalTaskRssParser.git",
    description="This is rss_reader",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="rss reader",
    python_requires='>=3.8',
)
