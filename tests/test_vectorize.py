import unittest
import os
from gippy import Options
from gippy import GeoImage
import beachfront
from nose.tools import set_trace


class TestMask(unittest.TestCase):
    """ Test masking functions """

    def setUp(self):
        Options.set_verbose(4)


    def test_trace(self):
        """ Trace binary image """
        geoimg = GeoImage('test.tif', 100, 100)
        