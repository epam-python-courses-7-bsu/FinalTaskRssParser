from setuptools import setup

setup(
    name="Rss-reader",
    version="1.0",
    author="Anatoli Ageichik",
    author_email="3anatoliageichik@gmail.com",
    description="Rss reader, which write in Python",
    url="https://github.com/AnatoliAgeichik/FinalTaskRssParser",
    packages=['rss_reader'],
    python_requires='>=3.8.0',
    install_requires=['feedparser']
)