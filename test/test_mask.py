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
import unittest
import os
from gippy import Options
from beachfront import mask
from .utils import download_image


class TestMask(unittest.TestCase):
    """ Test masking functions """

    # some cirrus clouds
    imgurl = 'http://landsat-pds.s3.amazonaws.com/L8/008/028/LC80080282016215LGN00/LC80080282016215LGN00_B3.TIF'
    qimgurl = 'http://landsat-pds.s3.amazonaws.com/L8/008/028/LC80080282016215LGN00/LC80080282016215LGN00_BQA.TIF'

    vfilename = os.path.join(os.path.dirname(__file__), 'test-coast.geojson')

    #bbox = [-78.5964604299, -11.1797039494, -76.5056457676, -9.06874079313]
    bbox = [-65.1126692276, 44.929454947, -62.0891890425, 47.100321387]

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

    def test_mask(self):
        """ Create mask image from bitwise mask """
        bqaimg = download_image(self.qimgurl)
        maskimg = mask.create_mask_from_bitmask(bqaimg)
        arr = maskimg.read()
        self.assertTrue(arr.sum(), 23096984)
