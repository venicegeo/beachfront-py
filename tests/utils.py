import os
import numpy
from gippy import GeoImage

default_fout = os.path.join(os.path.dirname(__file__), 'test.tif')


def create_image(fout=None, xsz=10, ysz=10, nodata=99):
    """ Create test image """
    fout = default_fout if fout is None else fout
    geoimg = GeoImage.create(fout, xsz=xsz, ysz=ysz, dtype='byte')
    geoimg.set_nodata(nodata)
    return geoimg


def create_empty_image():
    """ Create emptry image """
    geoimg = create_image()
    arr = numpy.zeros((geoimg.xsize(), geoimg.ysize()), dtype='uint8')
    geoimg[0].write(arr)
    return geoimg
