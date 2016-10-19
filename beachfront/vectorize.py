from osgeo import ogr, osr
from gippy import GeoImage, GeoVector
import potrace as _potrace
import json
import fiona
from fiona.crs import from_epsg
from nose.tools import set_trace
import skimage.filters as filters
from skimage.morphology import dilation, square


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
        # ptypes = {k: fiona.prop_type(v) for k, v in output.schema['properties'].items()}
        output.writerecords(features)


def potrace_array(arr, turdsize=10.0):
    """ Trace numpy array using potrace """
    # arr2 = filters.laplace(arr) > 0
    bmp = _potrace.Bitmap(arr)
    polines = bmp.trace(turdsize=turdsize, turnpolicy=_potrace.TURNPOLICY_WHITE,
                        alphamax=0.0, opticurve=0.0)
    lines = []
    for line in polines:
        lines.append(line.tesselate().tolist())

    return lines


def potrace(geoimg, turdsize=1.0, geoloc=True):
    """ Trace raster image using potrace and return geojson """
    # assuming single band
    arr = geoimg.read()
    mask = geoimg.nodata_mask()
    arr[mask == 1] = 0
    lines = potrace_array(arr, turdsize=turdsize)

    if mask.max() > 0:
        mask = dilation(mask, square(3))
        newlines = []
        for line in lines:
            startloc = 0
            for loc in range(0, len(line)):
                # check if this is masked point
                if mask[line[loc][1], line[loc][0]]:
                    if (loc-startloc) > 1:
                        newlines.append(line[startloc:loc])
                    startloc = loc + 1
        # add the last line
        if (loc-startloc) > 1:
            newlines.append(line[startloc:])
        lines = newlines

    # convert potrace path to geojson
    source = geoimg.basename()
    geojson = {
        'type': 'FeatureCollection',
        'features': [],
    }
    gid = 0
    for line in lines:
        if geoloc:
            newline = []
            for point in line:
                pt = geoimg.geoloc(point[0], point[1])
                newline.append([pt.x(), pt.y()])
            line = newline
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': line
            },
            'properties': {
                'id': gid,
                'source': source
            }
        }
        geojson['features'].append(feature)
        gid += 1

    return geojson
