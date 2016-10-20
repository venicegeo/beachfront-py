import numpy as np


def otsu_threshold(georaster):
    """ Use Otsu's method to caluclate optimal threshold ignoring nodata values """
    nbins = 500
    hist = georaster.histogram(bins=nbins).astype(float)

    stats = georaster.stats()
    gain = (stats[1] - stats[0]) / nbins
    bin_centers = [stats[0] + i * gain for i in range(0, nbins)]

    # class probabilities for all possible thresholds
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # class means for all possible thresholds
    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]

    # Clip ends to align class 1 and class 2 variables:
    # The last value of `weight1`/`mean1` should pair with zero values in
    # `weight2`/`mean2`, which do not exist.
    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    idx = np.argmax(variance12)
    threshold = bin_centers[:-1][idx]

    return threshold
