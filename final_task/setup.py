from setuptools import setup, find_packages
import os

setup(
    name="rss-reader",
    version=open(os.path.join(os.getcwd(), "rss_reader", "VERSION.txt")).readline(),
    packages=find_packages(),
    author="Vlad Protosevich",
    author_email="protosevic2001@gmail.com",
    install_requires=['feedparser==5.2.1', 'colored==1.4.0', 'fpdf==1.7.2', 'requests==2.22.0'],
    entry_points={
        'console_scripts': [
            'rss-reader = rss_reader.rss_reader:run'
        ]
    },
    include_package_data=True,
)