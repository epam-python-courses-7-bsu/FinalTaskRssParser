import setuptools


with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="rss-reader",
    version="0.1",
    author="Artsiom D",
    description="RSS reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8"
)

