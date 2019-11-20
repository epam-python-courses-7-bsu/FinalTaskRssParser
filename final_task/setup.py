from setuptools import setup

setup(
    name='rss-reader',
    version='v4.0',
    packages=['rss_reader'],
    package_data={'rss_reader': ['ARIALUNI.ttf']},
    install_requires=['feedparser == 5.2.1', 'html2text == 2019.9.26', 'fpdf==1.7.2'],
    url='www.github.com',
    license='LICENCE.txt',
    author='AlexSpaceBy',
    author_email='fiz.zagorodnAA@gmail.com',
    description='RSS Reader',
    entry_points={'console_scripts': ['rss-reader = rss_reader.rss_reader:main']}
)
