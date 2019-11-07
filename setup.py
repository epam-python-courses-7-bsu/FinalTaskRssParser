from setuptools import setup, find_namespace_packages

setup(
    name='rss-reader',
    version='v3.0',
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=['feedparser == 5.2.1', 'html2text == 2019.9.26'],
    url='www.github.com',
    license='LICENCE.txt',
    author='AlexSpaceBy',
    author_email='fiz.zagorodnAA@gmail.com',
    description='RSS Reader',
    entry_points={'console_scripts': ['rss-reader = rss_reader.rss_reader:main']}
)
