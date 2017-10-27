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