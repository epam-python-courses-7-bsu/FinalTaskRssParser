from setuptools import setup, find_packages


setup(
    name="rss_reader",
    version="0.2.0",
    author="Sergey Rogonov",
    author_email="serega.rogonov@gmail.com",
    description="Python command line rss reader.",
    zip_safe=False,
    scripts=[
        'rss_reader/rss_reader.py',
        'rss_reader/news_articles.py',
        'rss_reader/parser.py',
        ],
    entry_points={
            'console_scripts': ['rss_reader=rss_reader:main'],
            },
    python_requires=">=3.8",
    install_requires=[
        'beautifulsoup4>=4.8.1',
        'bs4>=0.0.1',
        'lxml>=4.4.1',
        'soupsieve>=1.9.5',
    ]
)
