import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rss_reader_Anton_Zimahorau",
    version="2.2",
    author="Anton Zimahorau",
    author_email="antonzimahorau@gmail.com",
    description="Command-line utility which receives RSS URL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntonZimahorau/FinalTaskRssParser.git",
    packages=['rss_reader', 'rss_reader.functions', 'rss_reader.classes'],
    install_requires=['feedparser', 'lxml', 'argparse', 'requests', 'EbookLib==0.17.1',
                      'dominate==2.4.0', 'termcolor==1.1.0', 'coloredlogs==10.0'],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['rss-reader = rss_reader.rss_reader:main']
    }
)
