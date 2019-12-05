from setuptools import setup, find_packages


setup(
    name="rss_reader",
    version="0.4.0",
    author="Sergey Rogonov",
    author_email="serega.rogonov@gmail.com",
    url='https://github.com/SergeyRogonov/FinalTaskRssParser',
    description="Python command line rss reader.",
    zip_safe=False,
    packages=["rss_reader"],
    package_data={
        'rss_reader': ['templates/template.html'],
        },
    entry_points={
        'console_scripts': ['rss_reader=rss_reader.rss_reader:main'],
        },
    python_requires=">=3.8",
    install_requires=[
        'beautifulsoup4==4.8.1',
        'lxml==4.4.1',
        'Jinja2==2.10.3',
        'WeasyPrint==50',
        'python-dateutil',
    ]
)
