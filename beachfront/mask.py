from osgeo import ogr, osr
from gippy import GeoImage, GeoVector
import gippy.algorithms as alg
import json
from nose.tools import set_trace


def open_wfs(wfsurl, layername):
    """ Open a WFS 2.0 endpoint (EPSG 4326) """
    vec = ogr.Open(wfsurl)
    layer = vec.GetLayer(layername)
    return vec, layer


def get_features(layer, bbox):
    """ Get features in bounding box """
    # assumes bounding box in same projection as layer
    #filter = 'ST_Intersects(the_geoms, ST_MakeEnvelope([%s], 3857))' % ','.join(str(p) for p in bbox)
    # for now, assume bounding box in 3857
    layer.SetSpatialFilterRect(bbox[0], bbox[1], bbox[2], bbox[3])
    # convert to geojson ?
    return layer


def get_unioned_features(layer, bbox):
    """ Get union of all features in bounding box """
    layer = get_features(layer, bbox)
    poly = ogr.Geometry(ogr.wkbPolygon)
    for feature in layer:
        geom = feature.GetGeometryRef().GetLinearGeometry()
        poly = poly.Union(geom)
    return json.loads(poly.ExportToJson())


def transform_coords(bbox):
    """ Convert coordinates in arbitrary projection to EPSG:4326 """
    srs1 = osr.SpatialReference()
    srs1.ImportFromEPSG(3857)
    #srs2 = layer.GetSpatialRef()
    srs2 = osr.SpatialReference()
    srs2.ImportFromEPSG(4326)
    transform = osr.CoordinateTransformation(srs1, srs2)
    x0, y0, z0 = transform.TransformPoint(bbox[0], bbox[1])
    x1, y1, z1 = transform.TransformPoint(bbox[2], bbox[3])

    #inproj = Proj(init='EPSG:3857')
    #outproj = Proj(init=layer.GetSpatialRef())
    #x0, y0 = transform(inproj, outproj, bbox[0], bbox[1])
    #x1, y1 = transform(inproj, outproj, bbox[2], bbox[3])
    #features = geovec.where(filter)
    return [x0, y0, x1, y1]
    

#def fetch_vector(wfsurl, bbox=None):
#    """ Get polygons of WFS url intersecting bounding box """
    


def mask(fname, vector):
    geoimg = GeoImage(fname)
    geovec = GeoVector(vector)
    imgout = alg.cookie_cutter([geoimg], geovec)


def mask_bitmask(geoimg, bitmask):
    """ Create mask from a bitmask """
    return
