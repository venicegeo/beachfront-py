#!/usr/bin/env python
import os
from codecs import open
from setuptools import setup, find_packages
import imp

here = os.path.abspath(os.path.dirname(__file__))
__version__ = imp.load_source('beachfront.version', 'beachfront/version.py').__version__

# get the dependencies and installs
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    reqs = f.read().split('\n')

install_requires = [x.strip() for x in reqs if 'git+' not in x]

setup(
    name='beachfront',
    version=__version__,
    author='Matthew Hanson (matthewhanson)',
    description='library extracting coastline regions from raster data',
    url='https://github.com/venicegeo/bf-py',
    classifiers=[
        'Framework :: Pytest',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=['nose'],
)
