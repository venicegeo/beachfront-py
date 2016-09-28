import unittest
import os
from gippy import Options
from gippy import GeoImage
import beachfront
from nose.tools import set_trace


class TestProcess(unittest.TestCase):
    """ Test masking functions """

    def setUp(self):
        Options.set_verbose(4)
        self.test_image = GeoImage('test.tif', 100, 100)
        # TODO - create step function or other pattern in binary image 

    def test_threshold(self):
        """ Threshod binary image """
        geoimg = self.test_image()
        imgout = beachfront.process.threshold(geoimg)
        self.assertEqual(imgout.nbands(), 1)

