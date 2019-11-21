from setuptools import find_namespace_packages, setup

setup(
    name='rss_reader',
    version='3.0',
    description='RSS reader',
    author='Matyushenok Sergey',
    author_email='matyushenoksergei@yandex.by',
    package_dir={'rss_reader': 'rss_reader'},
    scripts=['rss_reader/News.py',
             'config.txt',
             'rss_reader/pars_args.py',
             'rss_reader/parser_rss.py',
             'rss_reader/exceptions.py',
             'rss_reader/database.py',
             'rss_reader/rss_reader.py'],
    entry_points={
        'console_scripts': ['rss-reader=rss_reader:main'],
    },
    packages=find_namespace_packages(),
    install_requires=['feedparser', 'python-dateutil', 'psycopg2-binary'],
    license="none",
    platforms="Linux, Windows (not tested)",
)
