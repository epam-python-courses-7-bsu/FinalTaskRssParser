from setuptools import setup

setup(
    name='rss-reader',
    version='v5.0',
    packages=['rss_reader'],
    include_package_data=True,
    install_requires=['feedparser', 'bs4', 'python-dateutil', 'fpdf', 'jinja2', 'colorama', 'termcolor', 'coloredlogs'],
    url='',
    author='Evgeny Androsik',
    author_email='androsikei95@gmail.com',
    description='RSS Reader',
    entry_points={'console_scripts': ['rss-reader = rss_reader.rss_reader:main']}
)
