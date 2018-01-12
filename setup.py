## Copyright [2017-2018] UMR MISTEA INRA, UMR LEPSE INRA,                ##
##                       UMR AGAP CIRAD, EPI Virtual Plants Inria        ##
##                                                                       ##
## This file is part of the StatisKit project. More information can be   ##
## found at                                                              ##
##                                                                       ##
##     http://statiskit.rtfd.io                                          ##
##                                                                       ##
## The Apache Software Foundation (ASF) licenses this file to you under  ##
## the Apache License, Version 2.0 (the "License"); you may not use this ##
## file except in compliance with the License. You should have received  ##
## a copy of the Apache License, Version 2.0 along with this file; see   ##
## the file LICENSE. If not, you may obtain a copy of the License at     ##
##                                                                       ##
##     http://www.apache.org/licenses/LICENSE-2.0                        ##
##                                                                       ##
## Unless required by applicable law or agreed to in writing, software   ##
## distributed under the License is distributed on an "AS IS" BASIS,     ##
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or       ##
## mplied. See the License for the specific language governing           ##
## permissions and limitations under the License.                        ##

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
        'console_scripts': ['conda-download = conda_tools.cli:download',
                            'conda-release = conda_tools.cli:release']},
    install_requires=[],
    zip_safe=False,
)
