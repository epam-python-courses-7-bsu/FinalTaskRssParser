from setuptools import setup

setup(name='Rss reader',
      version='1.4.2',
      description='Pure Python command-line RSS reader.',
      author='Marina Romanchuk',
      author_email='marina-romanchuk-2015@mail.ru',
      install_requires=['feedparser', 'doc', 'yattag', 'requests', 'fpdf'],
      zip_safe=False,
      scripts=[r'rss_reader\rss_parser.py',
               'rss_reader\console_interface.py',
               'rss_reader\database_functions.py',
               r'rss_reader\rss_reader.py'],
      entry_points={'console_scripts': ['rss-reader=rss_reader:main']}
)