from setuptools import setup

setup(
    name="FinalTaskRssParser",
    version="1.0",
    author="Usevalad Trafimau",
    author_email="Unioltered@gmail.com",
    description="This project helps to understand about setup.py.",
    url="https://github.com/Useftro/FinalTaskRssParser",
    packages=['rss_reader'],
    python_requires='>=3.8.0', install_requires=['feedparser', 'beautifulsoup4', 'fpdf', 'Pillow']
)