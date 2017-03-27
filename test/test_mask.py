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
import unittest
import os
from gippy import Options
from beachfront import mask
from .utils import download_image
from beachfront.logger import init_logger


class TestMask(unittest.TestCase):
    """ Test masking functions """

    # some cirrus clouds
    imgurl = 'http://landsat-pds.s3.amazonaws.com/L8/008/028/LC80080282016215LGN00/LC80080282016215LGN00_B3.TIF'
    qimgurl = 'http://landsat-pds.s3.amazonaws.com/L8/008/028/LC80080282016215LGN00/LC80080282016215LGN00_BQA.TIF'

    vfilename = os.path.join(os.path.dirname(__file__), 'test-coast.geojson')

    #bbox = [-78.5964604299, -11.1797039494, -76.5056457676, -9.06874079313]
    bbox = [-65.1126692276, 44.929454947, -62.0891890425, 47.100321387]

    @classmethod
    def setUpClass(cls):
        """ Initialize logging """
        init_logger(muted=True)

    def setUp(self):
        Options.set_verbose(2)

    def test_open_vector(self):
        """ Open WFS and check number of features """
        ds, layer = mask.open_vector(self.vfilename)
        self.assertEqual(layer.GetFeatureCount(), 16)

    def test_get_features(self):
        """ Open WFS using bounding box """
        ds, layer = mask.open_vector(self.vfilename)
        features = mask.get_features_as_geojson(layer, bbox=self.bbox)
        self.assertEqual(layer.GetFeatureCount(), 14)

    def test_get_features_unioned(self):
        """ Get union of all features within bounding box """
        ds, layer = mask.open_vector(self.vfilename)
        poly = mask.get_features_as_geojson(layer, bbox=self.bbox, union=True)
        self.assertAlmostEqual(poly['coordinates'][0][0][0], -65.0, 4)

    def test_mask_with_vector(self):
        """ Mask image with a WFS using gippy cookie_cutter """
        geoimg = download_image(self.imgurl)
        geoimg.set_nodata(0)
        imgout = mask.mask_with_vector(geoimg, (self.vfilename, ''))
        self.assertEqual(imgout.nbands(), 1)

    def _test_mask(self):
        """ Create mask image from bitwise mask """
        bqaimg = download_image(self.qimgurl)
        maskimg = mask.create_mask_from_bitmask(bqaimg)
        arr = maskimg.read()
        self.assertTrue(arr.sum(), 23096984)
