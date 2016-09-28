from osgeo import ogr, osr
from gippy import GeoImage, GeoVector
import gippy.algorithms as alg
import json
from skimage.filters import threshold_otsu


def threshold(fname, vector):
    """ Standard thresholding algorithm """
    # DRAFT
    geoimg = GeoImage(fname)
    nodata = geoimg[0].NoDataValue()

    img = geoimg[0].Read()
    ndinds = img == nodata
    img[ndinds] = 0
    th = threshold_otsu(img)

    inds = img > th
    img[inds] = 1
    img[~inds] = 0
    img[ndinds] = 1

    return img

