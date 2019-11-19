from setuptools import setup, find_namespace_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

setup(
   name='rss_reader',
   version='1.0',
   description='RSS reader',
   author='Roman Shagun',
   author_email='rshag17@gmail.com',
   package_dir={'': 'rss_reader'},
   scripts=['rss_reader/rss_feed.py', 'rss_reader/rss_item.py', 'rss_reader/exceptions_.py'],
   entry_points={
        'console_scripts': ['rss-reader=rss_reader.rss_reader:main'],
   },
   install_requires=['feedparser==5.2.1', 'argparse==1.4.0', 'jsonpickle==1.2', 'tinydb==3.15.1'],
   license="none",
   platforms="Linux, Windows (not tested)",
   long_description="Yet another RSS reader"
)
