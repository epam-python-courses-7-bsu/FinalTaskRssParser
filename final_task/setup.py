from setuptools import setup, find_packages
from os import path


directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README.md'), encoding='utf-8') as project_description:
    long_description = project_description.read()

setup(
    name='rss-reader_5.0',
    version='5.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Jinja2==2.10.3',
        'beautifulsoup4==4.8.1',
        'feedparser==5.2.1',
        'requests==2.22.0',
        'dominate==2.4.0',
        'fpdf==1.7.2',
        'termcolor==1.1.0',
        'coloredlogs==10.0',
    ],
    url='https://github.com/brechka/FinalTaskRssParser',
    author='Yuliya Brechka',
    author_email='juliabrechka@gmail.com',
    description='RSS reader',
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'rss-reader = rss_reader.rss_reader:main',
        ],
    },
    test_suite='rss_reader.tests',
    python_requires='>=3.8',
)
