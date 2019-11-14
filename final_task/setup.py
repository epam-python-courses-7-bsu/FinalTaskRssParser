from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='RSS-reader',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author="Oleg Slavashevich",
    author_email="oslavashevish@gmail.com"
)