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

from conda_tools import download

import unittest
from nose.plugins.attrib import attr

@attr(linux=True,
      osx=True,
      win=True,
      level=1)
class testWriteMetaPackage(unittest.TestCase):

    def test_download_run(self, directory='./share/git/FP17'):
        """Test conda_tools.download function with run dependencies"""
        download(directory, build=False, test=False, channel_urls=["statiskit"])

    # def test_download_build(self, directory='./share/git/FP17'):
    #     """Test conda_tools.download function with build dependencies"""
    #     download(directory, run=False, test=False, channel_urls=["statiskit"])

    def test_download_test(self, directory='./share/git/FP17'):
        """Test conda_tools.download function with test dependencies"""
        download(directory, build=False, run=False, channel_urls=["statiskit"])