from setuptools import find_namespace_packages, setup

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

with open('final_task/rss_reader/requirements.txt') as fp:
    install_requires = fp.read()

setup(
   name='rss_reader',
   version='1.0',
   description='RSS reader',
   author='Roman Shagun',
   author_email='rshag17@gmail.com',
   package_dir={'rss_reader': 'rss_reader'},
   entry_points={
        'console_scripts': ['rss-reader=final_task.rss_reader.rss_reader:main'],
   },
   packages=find_namespace_packages(),
   install_requires=install_requires,
   license="none",
   platforms="Linux, Windows (not tested)",
   long_description="Yet another RSS reader"
)
