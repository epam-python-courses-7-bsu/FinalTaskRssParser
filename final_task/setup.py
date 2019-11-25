from setuptools import setup

setup(
    name="FinalTaskRssParser",
    version="1.0",
    author="Usevalad Trafimau",
    author_email="Unioltered@gmail.com",
    description="rss_reader",
    url="https://github.com/Useftro/FinalTaskRssParser",
    packages=['rss_reader'],
    python_requires='>=3.8.0', install_requires=['feedparser==5.2.1', 'bs4==0.0.1', 'fpdf==1.7.2', 'Pillow==6.2.1',
                                                 'colorama==0.4.1']
)
