#!/usr/bin/env python
import sys

from setuptools import setup

if sys.version_info[:2] < (2, 7):
    sys.exit("conda-tools is only meant for Python >=2.7"
             "Current Python version: %d.%d" % sys.version_info[:2])

setup(
    name="conda-tools",
    version="0.9.0",
    author="Pierre Fernique",
    author_email="pfernique@gmail.com",
    url="https://github.com/StatisKit/conda-tools",
    license="Apache License 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    description="Multiple tools for easing the usage of Conda for developers",
    long_description=open('README.rst').read(),
    package_dir = {'': 'src/py'},
    packages=['conda_tools'],
    entry_points={
        'console_scripts': ['conda-download = conda_tools.cli:download']},
    install_requires=[],
    zip_safe=False,
)
