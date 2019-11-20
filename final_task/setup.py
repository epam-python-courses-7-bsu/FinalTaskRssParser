from setuptools import setup

setup(name='Rss reader',
      version='1.1',
      description='Pure Python command-line RSS reader.',
      author='Marina Romanchuk',
      author_email='marina-romanchuk-2015@mail.ru',
      install_requires=['feedparser', 'logging', 'json', 'argparse'],
      zip_safe=False,
      entry_points={'console_scripts': ['rss-reader=rss_reader:main']}
)