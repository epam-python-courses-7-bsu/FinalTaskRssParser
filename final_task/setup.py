from setuptools import setup, find_packages
from os import path


directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README.md'), encoding='utf-8') as project_description:
    long_description = project_description.read()

setup(
    name='rss-reader_2.1',
    version='2.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Jinja2==2.10.3', 'beautifulsoup4==4.8.1', 'feedparser', 'requests'],
    url='https://github.com/brechka/FinalTaskRssParser',
    author='Yuliya Brechka',
    author_email='juliabrechka@gmail.com',
    description='RSS reader',
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    entry_points={
        'console_scripts':
            ['rss-reader = rss_reader.rss_reader:main']
    },
    python_requires='>=3.8',
)
