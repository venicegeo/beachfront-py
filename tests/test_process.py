from __future__ import print_function
import unittest
import os
from gippy import Options
from gippy import GeoImage
from beachfront import process
from .utils import create_empty_image
from nose.tools import set_trace


class TestProcess(unittest.TestCase):
    """ Test masking functions """

    testname = os.path.join(os.path.dirname(__file__), 'test.tif')

    def _setUp(self):
        Options.set_verbose(4)
        self.test_image = GeoImage('test.tif', 100, 100)
        # TODO - create step function or other pattern in binary image

    def create_bimodal_image(self):
        """ Create image with a bimodal distribution """
        geoimg = create_empty_image()
        arr = geoimg.read()
        arr[0:3, 0:10] = 1
        arr[3:5, 0:10] = 2
        arr[5:7, 0:10] = 9
        arr[7:10, 0:10] = 10
        geoimg[0].write(arr)
        return geoimg

    def test_threshold(self):
        """ Threshod binary image """
        geoimg = self.create_bimodal_image()
        threshold = process.otsu_threshold(geoimg[0])
        bimg = geoimg[0].read() > threshold
        self.assertEqual(bimg.mean(), 0.5)
