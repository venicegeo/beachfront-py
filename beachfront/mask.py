from osgeo import ogr
from gippy import GeoImage, GeoVector
import gippy.algorithms as alg
import json
import numpy as np


def fetch_wfs(wfsurl, layer):
    """ Fetch wfs features within bounding box """
    wfs = ogr.Open(wfsurl)
    layer = wfs.GetLayer(layer)
    return (wfs, layer)


def get_features(layer, bbox=None, union=False):
    """ Union together all features in this layer and reutrn as GeoJSON """
    if bbox is not None:
        layer.SetSpatialFilterRect(bbox[0], bbox[3], bbox[2], bbox[1])
    poly = ogr.Geometry(ogr.wkbPolygon)
    if union:
        for feature in layer:
            geom = feature.GetGeometryRef()
            #  required for ogr2
            geom = geom.GetLinearGeometry()
            poly = poly.Union(geom)
    if bbox is not None:
        wkt = "POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))" % \
              (bbox[0], bbox[1], bbox[2], bbox[1], bbox[2], bbox[3], bbox[3], bbox[0], bbox[0], bbox[1])
        bbox_wkt = ogr.CreateGeometryFromWkt(wkt)
        poly = poly.Intersection(bbox_wkt)
    return json.loads(poly.ExportToJson())


def mask_with_wfs(geoimg, wfsurl, layer, fout=''):
    """ Mask geoimage with a WFS """
    ext = geoimg.geo_extent()
    wfs, layer = fetch_wfs(wfsurl, layer)
    feature = get_features(layer, bbox=[ext.x0(), ext.y0(), ext.x1(), ext.y1()], union=True)
    with open('feature.geojson', 'w') as f:
        f.write(json.dumps(feature))

    # create GeoVector
    geovec = GeoVector('feature.geojson')

    res = geoimg.resolution()
    imgout = alg.cookie_cutter([geoimg], feature=geovec[0],
                               proj=geoimg.srs(), xres=res.x(), yres=res.y())
    return imgout


def mask_with_landsat_bqa(geoimg, bqaimg):
    """ Mask geoimg with a series of provided bitmasks """
    # medium and high confidence clouds
    clouds = int('1000000000000000', 2)
    cirrus = int('0011000000000000', 2)

    # calculate mask
    arr = bqaimg.read()
    mask = (np.bitwise_and(arr, clouds) >= clouds) | (np.bitwise_and(arr, cirrus) >= cirrus)

    # create mask file
    maskimg = GeoImage.create_from(bqaimg, filename='cloudtest.tif', dtype='uint8')
    maskimg.set_nodata(0)
    maskimg[0].write(mask.astype('uint8'))

    return maskimg
