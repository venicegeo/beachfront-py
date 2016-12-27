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
import os
import tempfile
from osgeo import ogr
from gippy import GeoImage, GeoVector
import gippy.algorithms as alg
import json
import numpy as np


def open_vector(filename, layer=''):
    """ Fetch wfs features within bounding box """
    ds = ogr.Open(filename)
    if layer == '':
        layer = ds.GetLayer(0)
    else:
        layer = ds.GetLayer(layer)
    return (ds, layer)


def get_features_as_geojson(layer, bbox=None, union=False):
    """ Get features in this layer and return as GeoJSON """
    if bbox is not None:
        layer.SetSpatialFilterRect(bbox[0], bbox[3], bbox[2], bbox[1])
    poly = ogr.Geometry(ogr.wkbPolygon)
    if union:
        for feature in layer:
            geom = feature.GetGeometryRef()
            #  required for ogr2
            if hasattr(geom, 'GetLinearGeometry'):
                geom = geom.GetLinearGeometry()
            poly = poly.Union(geom)
    if bbox is not None:
        wkt = "POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))" % \
              (bbox[0], bbox[1], bbox[2], bbox[1], bbox[2], bbox[3], bbox[0], bbox[3], bbox[0], bbox[1])
        bbox_wkt = ogr.CreateGeometryFromWkt(wkt)
        poly = poly.Intersection(bbox_wkt)
    return json.loads(poly.ExportToJson())


def get_features(layer, bbox=None, union=False, filename=''):
    """ Get features in this layer and return as GeoVector """
    features = get_features_as_geojson(layer, bbox=bbox, union=union)
    if filename == '':
        f, filename = tempfile.mkstemp(suffix='.geojson')
        os.write(f, json.dumps(features))
        os.close(f)
    else:
        with open(filename, 'w') as f:
            f.write(json.dumps(features))
    # create GeoVector
    return GeoVector(filename)


def mask_with_vector(geoimg, vector, filename=''):
    """ Mask geoimage with a vector """
    ext = geoimg.geo_extent()
    ds, layer = open_vector(vector[0], vector[1])

    geovec = get_features(layer, bbox=[ext.x0(), ext.y0(), ext.x1(), ext.y1()], union=True)

    res = geoimg.resolution()
    imgout = alg.cookie_cutter([geoimg], filename=filename, feature=geovec[0],
                               proj=geoimg.srs(), xres=res.x(), yres=res.y())
    return imgout


def create_mask_from_bitmask(geoimg, filename=''):
    """ Mask geoimg with a series of provided bitmasks """
    # medium and high confidence clouds
    nodata = int('0000000000000001', 2)
    clouds = int('1000000000000000', 2)
    cirrus = int('0011000000000000', 2)

    # calculate mask
    arr = geoimg.read().astype('int16')
    # it is a good data mask
    mask = (np.bitwise_and(arr, nodata) != nodata) & \
           (np.bitwise_and(arr, clouds) < clouds) & \
           (np.bitwise_and(arr, cirrus) < cirrus)

    # create mask file
    maskimg = GeoImage.create_from(geoimg, filename=filename, dtype='uint8')
    maskimg.set_nodata(0)
    maskimg[0].write(mask.astype('uint8'))

    return maskimg
