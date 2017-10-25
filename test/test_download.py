from test_distribution import AbstractTestContinuousUnivariateDistribution

from conda_download import download

import unittest
from nose.plugins.attrib import attr

@attr(linux=True,
      osx=True,
      win=True,
      level=1)
class TestDownload(unittest.TestCase):

    def test_download_run(directory='.'):
        """Test conda_download.download function with run dependencies"""
        download(directory, build=False)

    def test_download_build(directory='.'):
        """Test conda_download.download function with build dependencies"""
        download(directory, run=False)