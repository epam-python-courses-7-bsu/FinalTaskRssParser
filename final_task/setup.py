from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


setup(
   name='rss_reader',
   version='1.4',
   description='RSS reader',
   author='Roman Shagun',
   author_email='rshag17@gmail.com',
   packages=find_packages(),
   data_files=[('rss_reader', ['rss_reader/Arial-Unicode-Regular.ttf'])],
   entry_points={
        'console_scripts': ['rss-reader=rss_reader.rss_reader:main'],
   },
   install_requires=[
       'feedparser==5.2.1',
       'argparse==1.4.0',
       'jsonpickle==1.2',
       'tinydb==3.15.1',
       'requests==2.22.0',
       'dominate==2.4.0',
       'beautifulsoup4==4.8.1',
       'fpdf==1.7.2'],
   license="none",
   platforms="Linux, Windows (not tested)",
   long_description="Yet another RSS reader",
   include_package_data=True
)