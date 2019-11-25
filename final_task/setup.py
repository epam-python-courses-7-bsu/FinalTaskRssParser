from setuptools import setup, find_packages

setup(
    name='rss-reader',
    version='4.0',
    packages=find_packages(),
    description='RSS reader',
    url='https://github.com/AnatoliAgeichik/FinalTaskRssParser',
    author='AnatoliAgeichik',
    author_email='3anatoliageichik@gmail.com',
    python_requires='>=3.7.0',
    install_requires=['feedparser==5.2.1', 'fpdf==1.7.2', 'dominate==2.4.0'],
    entry_points={
        'console_scripts': [
            'rss-reader = rss_reader.rss_reader:main',
        ],
    },
    test_suite='rss_reader.tests'
)
