from skimage.filters import threshold_otsu
from nose.tools import set_trace


def otsu_threshold(georaster):
    """ Use Otsu's method to caluclate optimal threshold ignoring nodata values """
    img = georaster.read()
    nodata = georaster.nodata()
    ndinds = img != nodata
    # img[ndinds] = 0
    threshold = threshold_otsu(img)

    return threshold
