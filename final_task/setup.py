import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_rss_reader",
    version="1.0",
    author="Kirill Stepanishin",
    author_email="kirill.stpn.by@gmail.com",
    description="Pure Python command-line RSS reader.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kirill-stp/FinalTaskRssParser",
    packages=['rss_reader'],
    python_requires='>=3.8',
<<<<<<< HEAD
    install_requires=['feedparser','requests','dominate','fpdf','termcolor']
=======
    install_requires=['feedparser','requests','dominate','fpdf']
>>>>>>> ee7ddc5f3897764b3da12847a678a2487a76a762
)
