from osgeo import ogr
from gippy import GeoImage, GeoVector
import gippy.algorithms as alg
import json
import numpy as np


def open_vector(filename, layer):
    """ Fetch wfs features within bounding box """
    wfs = ogr.Open(filename)
    layer = wfs.GetLayer(layer)
    return (wfs, layer)


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
              (bbox[0], bbox[1], bbox[2], bbox[1], bbox[2], bbox[3], bbox[3], bbox[0], bbox[0], bbox[1])
        bbox_wkt = ogr.CreateGeometryFromWkt(wkt)
        poly = poly.Intersection(bbox_wkt)
    return json.loads(poly.ExportToJson())


def get_features(layer, bbox=None, union=False):
    """ Get features in this layer and return as GeoVector """
    features = get_features_as_geojson(layer, bbox=bbox, union=union)
    with open('feature.geojson', 'w') as f:
        f.write(json.dumps(features))
    # create GeoVector
    return GeoVector('feature.geojson')


def mask_with_vector(geoimg, vector, fout=''):
    """ Mask geoimage with a vector """
    ext = geoimg.geo_extent()
    wfs, layer = open_vector(vector[0], vector[1])
    geovec = get_features(layer, bbox=[ext.x0(), ext.y0(), ext.x1(), ext.y1()], union=True)

    res = geoimg.resolution()
    imgout = alg.cookie_cutter([geoimg], feature=geovec[0],
                               proj=geoimg.srs(), xres=res.x(), yres=res.y())
    return imgout


def create_mask_from_bitmask(geoimg):
    """ Mask geoimg with a series of provided bitmasks """
    # medium and high confidence clouds
    clouds = int('1000000000000000', 2)
    cirrus = int('0011000000000000', 2)

    # calculate mask
    arr = geoimg.read()
    mask = (np.bitwise_and(arr, clouds) >= clouds) | (np.bitwise_and(arr, cirrus) >= cirrus)

    # create mask file
    maskimg = GeoImage.create_from(geoimg, dtype='uint8')
    maskimg.set_nodata(0)
    maskimg[0].write(mask.astype('uint8'))

    return maskimg
