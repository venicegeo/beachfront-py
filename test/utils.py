import os
import numpy
import requests
from gippy import GeoImage

default_fout = os.path.join(os.path.dirname(__file__), 'test.tif')


def create_image(fout=None, xsz=10, ysz=10, nodata=99, empty=False):
    """ Create test image, empty means all nodata, otherwise 0  """
    fout = default_fout if fout is None else fout
    geoimg = GeoImage.create(fout, xsz=xsz, ysz=ysz, dtype='byte')
    geoimg.set_nodata(nodata)
    if not empty:
        arr = numpy.zeros((geoimg.xsize(), geoimg.ysize()), dtype='uint8')
        geoimg[0].write(arr)
    return geoimg


def download_image(url):
    """ Download a test image """
    fout = os.path.join(os.path.dirname(__file__), os.path.basename(url))
    if not os.path.exists(fout):
        print('Downloading image %s' % fout)
        stream = requests.get(url, stream=True)
        try:
            with open(fout, 'wb') as f:
                for chunk in stream.iter_content(1024):
                    f.write(chunk)
        except:
            raise Exception("Problem downloading %s" % url)
    return GeoImage(fout)