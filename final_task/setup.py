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
        'rss_reader': ['static/template.html'],
        },
    entry_points={
        'console_scripts': ['rss_reader=rss_reader.rss_reader:main'],
        },
    python_requires=">=3.8",
    install_requires=[
        'beautifulsoup4==4.8.1',
        'lxml==4.4.1',
        'soupsieve==1.9.5',
        'Jinja2==2.10.3',
        'WeasyPrint==50',  # almost all below comes with this package
        'cairocffi==1.1.0',
        'CairoSVG==2.4.2',
        'cffi==1.13.2',
        'cssselect2==0.2.2',
        'defusedxml==0.6.0',
        'html5lib==1.0.1',
        'MarkupSafe==1.1.1',
        'Pillow==6.2.1',
        'pycparser==2.19',
        'Pyphen==0.9.5',
        'python-dateutil==2.8.1',
        'six==1.13.0',
        'tinycss2==1.0.2',
        'webencodings==0.5.1',
    ]
)
