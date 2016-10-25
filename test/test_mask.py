import unittest
import os
from gippy import Options
from beachfront import mask
from .utils import download_image
from nose.tools import set_trace

# load envvars
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class TestMask(unittest.TestCase):
    """ Test masking functions """

    imgurl = 'http://landsat-pds.s3.amazonaws.com/L8/139/045/LC81390452014295LGN00/LC81390452014295LGN00_B3.TIF'

    wfsurl = os.environ.get('WFS_URL')
    layer = os.environ.get('LAYER')

    bbox = [-78.5964604299, -11.1797039494, -76.5056457676, -9.06874079313]
    bbox_32618 = [107085.0, -1236285.0, 334515.0, -1004385.0]

    def setUp(self):
        Options.set_verbose(5)

    def test_open_wfs(self):
        """ Open WFS and check number of features """
        wfs, layer = mask.fetch_wfs(self.wfsurl, self.layer)
        self.assertEqual(layer.GetFeatureCount(), 10686)

    def test_get_features(self):
        """ Open WFS using bounding box """
        wfs, layer = mask.fetch_wfs(self.wfsurl, self.layer)
        features = mask.get_features(layer, bbox=self.bbox)
        self.assertEqual(layer.GetFeatureCount(), 4)

    def test_get_features_unioned(self):
        """ Get union of all features within bounding box """
        wfs, layer = mask.fetch_wfs(self.wfsurl, self.layer)
        poly = mask.get_features(layer, bbox=self.bbox, union=True)
        self.assertAlmostEqual(poly['coordinates'][0][0][0], -77.5029, 4)

    def _test_rasterize_layer(self):
        """ Rasterize a layer (GDAL 2 only) """
        ds, layer = mask.fetch_wfs(self.wfsurl, self.layer, bbox=self.bbox)
        poly = mask.union_features(layer)        
        geoimg = mask.rasterize_layer(layer)

    def test_mask_with_wfs(self):
        """ Mask image with a WFS using gippy cookie_cutter """
        geoimg = download_image(self.imgurl)
        geoimg.set_nodata(0)
        imgout = mask.mask_with_wfs(geoimg, self.wfsurl, self.layer)
        self.assertEqual(imgout.nbands(), 1)
