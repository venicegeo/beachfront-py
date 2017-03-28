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
import numpy
import requests
from gippy import GeoImage


def create_image(fout='', xsz=10, ysz=10, nodata=99, empty=False):
    """ Create test image, empty means all nodata, otherwise 0  """
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
