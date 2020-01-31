from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rss-reader',
    version='4.0',
    packages=find_packages(),
    description='Python RSS reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IlyaTorch/FinalTaskRssParser',
    author='Ilya Torch',
    author_email='itorch2001@gmail.com',
    package_data={'rss_reader': ['DejaVuSans.ttf']},
    install_requires=['feedparser==5.2.1', 'fpdf==1.7.2', 'dominate==2.4.0'],
    entry_points={
        'console_scripts': [
            'rss-reader = rss_reader.rss_reader:main',
        ],
    },
    test_suite='rss_reader.tests'
)
