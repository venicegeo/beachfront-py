import unittest
import os
from gippy import Options
from gippy import GeoImage
import beachfront 
from nose.tools import set_trace


class TestMask(unittest.TestCase):
    """ Test masking functions """

    wfsurl = 'WFS:http://gsn-geose-loadbala-17usyyb36bfdl-1788485819.us-east-1.elb.amazonaws.com/geoserver/piazza/wfs?service=wfs&version=2.0.0'
    layername = '2d791d6c-dabb-4b28-8d23-d1d78d8d29ff'
    bbox = [-78.5964604299, -11.1797039494, -76.5056457676, -9.06874079313]
    bbox_32618 = [107085.0, -1236285.0, 334515.0, -1004385.0]

    def setUp(self):
        Options.set_verbose(4)

    def open_wfs(self):
        """ Open WFS """
        return beachfront.open_wfs(self.wfsurl, self.layername)

    def test_open_wfs(self):
        """ Open WFS and check number of features """
        ds, layer = self.open_wfs()
        self.assertEqual(layer.GetFeatureCount(), 9620)

    def test_get_features(self):
        """ Get only features within a bounding box """
        ds, layer = self.open_wfs()
        layer = beachfront.get_features(layer, self.bbox)
        self.assertEqual(layer.GetFeatureCount(), 4)

    def test_get_unioned_features(self):
        """ Get union of all features within bounding box """
        ds, layer = self.open_wfs()
        poly = beachfront.get_unioned_features(layer, self.bbox)
        self.assertEqual(poly['coordinates'][0][0][0], -78.0)

    def _test_coordinate_transform(self):
        """ Convert coordinates a UTM zone (zone 18N) to EPSG:4326 """
        bbox = beachfront.transform_coords(self.bbox_32618)
        self.assertAlmostEqual(self.bbox[0], bbox[0])
        self.assertAlmostEqual(self.bbox[1], bbox[1])
        self.assertAlmostEqual(self.bbox[2], bbox[2])
        self.assertAlmostEqual(self.bbox[3], bbox[3])

