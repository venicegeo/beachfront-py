from osgeo import ogr, osr
from gippy import GeoImage, GeoVector
import potrace
import json
import fiona
from fiona.crs import from_epsg

def create_shapefile(fname, features):
    schema = {
        'geometry': 'LineString', 
        'properties': {
            'id': 'int',
            'source': 'str:24',
        }
    }
    # TODO - get epsg from geojson
    crs = from_epsg(32750)    
    with fiona.open(fname, 'w', 'ESRI Shapefile', schema, crs=crs) as output:
        #ptypes = {k: fiona.prop_type(v) for k, v in output.schema['properties'].items()}
        output.writerecords(features)
        
        
def to_geojson(geoimg, path):
    geojson = {
        'type': 'FeatureCollection',
        'features': [],
    }
    source = 'landsat'
    gid = 0
    for curve in path:
        coords = curve_to_coords(curve, geoimg)
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            },
            'properties': {
                'id': gid,
                'source': source
            }
        }
        gid += 1
        geojson['features'].append(feature)
    return geojson


def curve_to_coords(curve, geoimg):
    """ Convert curve coordinates to projected """
    coords = []
    for c in curve.tesselate().tolist():
        pt = geoimg.GeoLoc(c[0], c[1])
        coords.append([pt.x(), pt.y()])
    return coords


def trace_it(img, turdsize=10.0):
    """ Trace raster image using potrace """
    potrace.Bitmap(img)
    bmp = potrace.Bitmap(img)
    path = bmp.trace(turdsize=turdsize, turnpolicy=potrace.TURNPOLICY_WHITE)
    geojson = to_geojson(path)
    return geojson