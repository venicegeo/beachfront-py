"""
beachfront-py
https://github.com/venicegeo/beachfront-py

Copyright 2016, RadiantBlue Technologies, Inc.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from __future__ import print_function
import unittest
import os
from beachfront import process
from beachfront.logger import init_logger
from .utils import create_image, download_image


class TestProcess(unittest.TestCase):
    """ Test masking functions """

    @classmethod
    def setUpClass(cls):
        """ Initialize logging """
        init_logger(muted=True)

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
