from __future__ import print_function
import unittest
import os
from gippy import Options
from gippy import GeoImage
from beachfront import process
from .utils import create_image, download_image


class TestProcess(unittest.TestCase):
    """ Test masking functions """

    testname = os.path.join(os.path.dirname(__file__), 'test.tif')

    def _setUp(self):
        Options.set_verbose(4)
        self.test_image = GeoImage('test.tif', 100, 100)
        # TODO - create step function or other pattern in binary image

    def create_bimodal_image(self):
        """ Create image with a bimodal distribution """
        geoimg = create_image()
        arr = geoimg.read()
        arr[0:3, 0:10] = 1
        arr[3:5, 0:10] = 2
        arr[5:7, 0:10] = 9
        arr[7:10, 0:10] = 10
        geoimg[0].write(arr)
        return geoimg

    def test_threshold(self):
        """ Threshold binary image """
        geoimg = self.create_bimodal_image()
        threshold = round(process.otsu_threshold(geoimg[0]))
        self.assertEqual(threshold, 2)

        # add some nodata regions
        arr = geoimg.read()
        arr[4:6, 0:10] = geoimg[0].nodata()
        geoimg[0].write(arr)
        # test otsu threshold with nodata, should be similar since
        # nodata regions were an even number of 2's and 9's that cancel
        threshold = round(process.otsu_threshold(geoimg[0]))
        self.assertEqual(threshold, 2)

    def test_real_image(self):
        """ Threshold a real image """
        url = 'http://landsat-pds.s3.amazonaws.com/L8/139/045/LC81390452014295LGN00/LC81390452014295LGN00_B3.TIF'
        geoimg = download_image(url)
        geoimg.set_nodata(0)

        threshold = process.otsu_threshold(geoimg[0])
        geoimg[0] = geoimg[0] > threshold

        ext = os.path.splitext(geoimg.filename())[1]
        fout = os.path.splitext(geoimg.filename())[0] + '_otsu' + ext
        geoimg.save(fout, dtype='uint8')
        print('\nPerform visual inspection on %s' % fout)
