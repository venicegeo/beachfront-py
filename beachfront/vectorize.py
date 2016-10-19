import json
from osgeo import osr
import potrace as _potrace
from pyproj import Proj, transform
import fiona
from fiona.crs import from_epsg
from skimage.morphology import dilation, square

# TODO - update this function
def _save_shapefile(fname, features):
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


def save_geojson(lines, fout, source='imagery'):
    """ Save lines as GeoJSON file """
    geojson = {
        'type': 'FeatureCollection',
        'features': [],
    }
    gid = 0
    for line in lines:
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
    with open(fout, 'w') as f:
        f.write(json.dumps(geojson))
    return fout


def potrace_array(arr, turdsize=10.0, tolerance=0.2):
    """ Trace numpy array using potrace """
    # arr2 = filters.laplace(arr) > 0
    bmp = _potrace.Bitmap(arr)
    polines = bmp.trace(turdsize=turdsize, turnpolicy=_potrace.TURNPOLICY_WHITE,
                        alphamax=0.0, opticurve=1.0, opttolerance=tolerance)
    lines = []
    for line in polines:
        lines.append(line.tesselate().tolist())

    return lines


def filter_nodata_lines(lines, mask):
    """ Apply mask (numpy array) to remove and split lines crossing nodata regions """
    if mask.max() == 0:
        raise Exception('Empty mask!')
    mask = dilation(mask, square(3))
    newlines = []
    for line in lines:
        startloc = 0
        for loc in range(0, len(line)):
            # check if this is masked point
            if mask[int(line[loc][1]), int(line[loc][0])]:
                if (loc-startloc) > 1:
                    newlines.append(line[startloc:loc])
                startloc = loc + 1
    # add the last line
    if (loc-startloc) > 1:
        newlines.append(line[startloc:])
    return newlines


def potrace(geoimg, geoloc=False, turdsize=1.0, tolerance=0.2):
    """ Trace raster image using potrace and return geolocated or lat-lon coordinates """
    # assuming single band
    arr = geoimg.read()
    mask = geoimg.nodata_mask()
    arr[mask == 1] = 0
    lines = potrace_array(arr, turdsize=turdsize, tolerance=tolerance)

    if mask.max() > 0:
        lines = filter_nodata_lines(lines, mask)

    if not geoloc:
        srs = osr.SpatialReference(geoimg.srs()).ExportToProj4()
        projin = Proj(srs)
        projout = Proj(init='epsg:4326')
    newlines = []
    for line in lines:
        newline = []
        for point in line:
            pt = geoimg.geoloc(point[0], point[1])
            pt = [pt.x(), pt.y()]
            if not geoloc:
                # convert to lat-lon
                pt = transform(projin, projout, pt[0], pt[1])
            newline.append(pt)
        newlines.append(newline)

    return newlines
