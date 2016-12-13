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
import glob
import json
import numpy
from gippy import Options
from beachfront import vectorize
from .utils import create_image, download_image


class TestVectorize(unittest.TestCase):
    """ Test masking functions """

    def setUp(self):
        Options.set_verbose(2)
        numpy.set_printoptions(precision=2)

    def create_image_with_line(self):
        """ Create image with small line in middle """
        geoimg = create_image()
        arr = numpy.zeros((geoimg.xsize(), geoimg.ysize()), dtype='uint8')
        # arr[40:60, 50] = 1
        arr[2:8, 5] = 1
        geoimg[0].write(arr)
        self.truth_coords = [
            [50.36996467799592, 50.0], [50.39062402284878, 46.0953125],
            [50.530935406641134, 43.548242187499994], [50.66263873007813, 43.83125],
            [50.73724191982458, 44.75], [50.73724191982458, 44.75],
            [50.93924440283034, 50.0], [50.73724191982458, 55.25],
            [50.73724191982458, 55.25], [50.66263873007813, 56.16875],
            [50.530935406641134, 56.451757812500006], [50.39062402284878, 53.9046875], [50.36996467799592, 50.0]
        ]
        return geoimg

    def create_image_with_box(self):
        """ Create image with box in middle """
        geoimg = create_image()
        arr = numpy.zeros((geoimg.xsize(), geoimg.ysize()), dtype='uint8')
        # arr[25:75, 25:75] = 1
        arr[2:8, 2:8] = 1
        geoimg[0].write(arr)
        self.truth_coords = [
            [0.2, 0.8], [0.5, 0.8], [0.8, 0.8], [0.8, 0.5], [0.8, 0.19999999999999996],
            [0.5, 0.19999999999999996], [0.2, 0.19999999999999996], [0.2, 0.5]
            # [0.2, 0.8], [0.5, 0.8], [0.8, 0.8], [0.8, 0.5], [0.8, 0.2], [0.5, 0.2], [0.2, 0.2], [0.2, 0.5]
            # [0.25, 0.75], [0.5, 0.75], [0.75, 0.75], [0.75, 0.5], [0.75, 0.25], [0.5, 0.25], [0.25, 0.25], [0.25, 0.5]
        ]
        return geoimg

    def test_potrace_arrays(self):
        """ Trace numpy arrays using potrace """
        arr = numpy.zeros((10, 10), dtype='uint8')
        lines = vectorize.potrace_array(arr)
        self.assertEqual(type(lines), list)
        self.assertEqual(len(lines), 0)

    def test_save_geojson(self):
        """ Validate geojson returned from trace """
        geoimg = create_image()
        lines = vectorize.potrace(geoimg[0])
        fout = os.path.join(os.path.dirname(__file__), 'test.geojson')
        vectorize.save_geojson(lines, fout, source='test')
        with open(fout, 'r') as f:
            geojson = json.loads(f.read())
        self.assertTrue('type' in geojson.keys())
        self.assertEqual(geojson['type'], 'FeatureCollection')
        self.assertTrue('features' in geojson.keys())
        self.assertEqual(len(geojson['features']), 0)
        os.remove(fout)
        # TODO - check populated geojson

    def test_save_shapefile(self):
        """ Save shapefile """
        geoimg = self.create_image_with_box()
        lines = vectorize.potrace(geoimg[0])
        fout = os.path.join(os.path.dirname(__file__), 'test-shapefile')
        vectorize.save_shapefile(lines, fout + '.shp')
        [os.remove(f) for f in glob.glob(fout + '.*')]

    # potrace does not trace lines, it's outer edge of polygons
    def _test_trace_line(self):
        """ Trace image of line """
        geoimg = self.create_image_with_line()
        geojson = vectorize.potrace(geoimg[0], geoloc=False)

        # check returned geometry
        coords = geojson['features'][0]['geometry']['coordinates']
        self.assertEqual(len(coords), len(self.truth_coords))
        for c in coords:
            self.assertTrue(c in self.truth_coords)

    def test_potrace_box(self):
        """ Trace image of box """
        geoimg = self.create_image_with_box()
        lines = vectorize.potrace(geoimg[0], geoloc=True)
        # check returned geometry
        self.assertEqual(len(lines[0]), len(self.truth_coords))
        for c in lines[0]:
            self.assertTrue(c in self.truth_coords)

    def test_potrace_turdsize(self):
        """ Trace line with turdsize smaller and larger than box """
        geoimg = self.create_image_with_box()

        # check that turdsize did not filter out box
        lines = vectorize.potrace(geoimg[0], turdsize=30, geoloc=False)
        self.assertEqual(len(lines[0]), len(self.truth_coords))

        # check that turdsize does filter out box
        lines = vectorize.potrace(geoimg[0], turdsize=50)
        self.assertEqual(len(lines), 0)

    def test_potrace_nodata(self):
        """ Trace image with nodata present """
        geoimg = self.create_image_with_box()
        arr = geoimg.read()
        # make a nodata region
        arr[0:5, 0:5] = geoimg[0].nodata()
        geoimg[0].write(arr)
        lines = vectorize.potrace(geoimg[0], geoloc=False)

        self.assertEqual(len(lines), 1)

        self.assertEqual(len(lines[0]), 5)
        self.assertEqual(lines[0],
                         [(0.8, 0.8), (0.8, 0.5), (0.8, 0.19999999999999996),
                         (0.5, 0.19999999999999996), (0.2, 0.19999999999999996)])

    def test_potrace_empty_image(self):
        """ Trace image that is empty """
        geoimg = create_image(empty=True)
        lines = vectorize.potrace(geoimg[0], geoloc=False)
        self.assertEqual(len(lines), 0)
        geoj = vectorize.to_geojson(lines)
        self.assertEqual(len(geoj['features']), 0)

    def test_potrace_only_nodata(self):
        """ Trace image that has only nodata """
        geoimg = create_image(empty=True)
        arr = geoimg.read()
        # make a nodata region
        arr[0:5, 0:5] = geoimg[0].nodata()
        geoimg[0].write(arr)
        lines = vectorize.potrace(geoimg[0], geoloc=False)
        self.assertEqual(len(lines), 0)
        geoj = vectorize.to_geojson(lines)
        self.assertEqual(len(geoj['features']), 0)

    def test_potrace_image(self):
        """ Trace landsat using an arbitrary cutoff """
        # get a complex test image (landsat)
        url = 'http://landsat-pds.s3.amazonaws.com/L8/139/045/LC81390452014295LGN00/LC81390452014295LGN00_B3.TIF'
        geoimg = download_image(url)
        geoimg.set_nodata(0)
        lines = vectorize.potrace(geoimg[0] > 9500)
        self.assertEqual(len(lines), 383)
        fout = os.path.splitext(os.path.join(os.path.dirname(__file__), os.path.basename(url)))[0] + '.geojson'
        vectorize.save_geojson(lines, fout)
        print('\nPerform visual inspection on %s' % fout)
