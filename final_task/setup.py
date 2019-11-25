from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='rss_reader',
      version='2.0',
      packages=find_packages(),
      description='RSS-reader',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Leonid-Shutov/FinalTaskRssParser',
      author='Leonid Shutov',
      author_email='14m64y87w@gmail.com',
      install_requires=['beautifulsoup4==4.8.1','lxml==4.4.1','requests==2.22.0','dominate==2.4.0','fpdf==1.7.2','httplib2==0.14.0'],
      entry_points={
      'console_scripts': [
                          'rss-reader = rss_reader.rss_reader:main',
                          ],
      },
      )

