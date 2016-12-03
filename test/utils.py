"""
beachfront-py
https://github.com/venicegeo/beachfront-py

Copyright 2016, RadiantBlue Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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
