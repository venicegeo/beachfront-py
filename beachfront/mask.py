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
import os
import tempfile
from osgeo import ogr
from gippy import GeoImage, GeoVector
import gippy.algorithms as alg
import json
import numpy as np
import logging


logger = logging.getLogger(__name__)


def open_vector(filename, layer=''):
    """ Fetch wfs features within bounding box """
    logger.info('Opening %s as vector file' % filename, action='Open file', actee=filename, actor=__name__)
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
        logger.info('Saving JSON as vector file', action='Save file', actee=filename, actor=__name__)
        # if no geometries, returns empty geometry collection
        if features['type'] == 'GeometryCollection':
            features = {'type': 'FeatureCollection', 'features': []}
        os.write(f, json.dumps(features))
        os.close(f)
    else:
        logger.info('Saving JSON as vector file', action='Save file', actee=filename, actor=__name__)
        logger.info('Writing GeoJSON to file %s' % filename)
        with open(filename, 'w') as f:
            f.write(json.dumps(features))
    # create GeoVector
    return GeoVector(filename)


def get_coastline(bbox):
    """ Get coastline GeoJSON within bounding box """
    cmask = open_vector(os.path.join(os.path.dirname(__file__), 'coastline.shp'))
    lons = [c[0] for c in bbox['features'][0]['geometry']['coordinates'][0]]
    lats = [c[1] for c in bbox['features'][0]['geometry']['coordinates'][0]]
    bbox = [min(lons), min(lats), max(lons), max(lats)]
    gj = get_features_as_geojson(cmask[1], bbox=bbox, union=True)
    return gj


def mask_with_vector(geoimg, vector, filename=''):
    """ Mask geoimage with a vector """
    ext = geoimg.geo_extent()
    ds, layer = open_vector(vector[0], vector[1])

    geovec = get_features(layer, bbox=[ext.x0(), ext.y0(), ext.x1(), ext.y1()], union=True)
    if geovec.nfeatures() == 0:
        raise RuntimeError('No features after masking')

    res = geoimg.resolution()
    logger.info('Saving to file %s' % filename, action='Save file', actee=filename, actor=__name__)
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
    logger.info('Saving to file %s' % filename, action='Save file', actee=filename, actor=__name__)
    maskimg = GeoImage.create_from(geoimg, filename=filename, dtype='uint8')
    maskimg.set_nodata(0)
    maskimg[0].write(mask.astype('uint8'))

    return maskimg
