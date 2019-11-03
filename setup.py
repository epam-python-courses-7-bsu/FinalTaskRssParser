from setuptools import setup, find_namespace_packages

setup(
    name='RssReader',
    version='v1.0',
    packages=find_namespace_packages(),
    include_package_data=True,
    url='www.github.com',
    license='LICENCE.txt',
    author='AlexSpaceBy',
    author_email='fiz.zagorodnAA@gmail.com',
    description='RSS Reader',
    entry_points={'console_scripts': ['RssReader = RssReader.__main__:main']}
)
