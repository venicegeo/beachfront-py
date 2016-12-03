"""
beachfront-py
https://github.com/venicegeo/beachfront-py

Copyright 2016, RadiantBlue Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import print_function
import unittest
import os
from gippy import Options
from gippy import GeoImage
from beachfront import process
from .utils import create_image, download_image


class TestProcess(unittest.TestCase):
    """ Test masking functions """

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
