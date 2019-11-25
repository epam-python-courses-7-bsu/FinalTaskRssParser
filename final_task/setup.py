from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rss-reader_scarzdz",
    version="0.3",
    url="https://github.com/scarzdz/FinalTaskRssParser",
    license="MIT",
    author="Denis Marfonov",
    author_email="marfonovdenis@gmail.com",
    description="Cli-based RSS Reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["rss_reader"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4",
        "feedparser",
        "lxml"
    ],
    entry_points={
        "console_scripts": [
            "rss-reader=rss_reader.rss_reader:main",
        ],
    }
)
