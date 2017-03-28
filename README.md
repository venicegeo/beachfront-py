# beachfront-py

beachfront-py is a library of functions used for the creation of vector shorelines automatically from imagery.

## Installation
There are several system libraries required should be installed before installing beachfront-py. On a debian system:

    $ apt-get install -y python-setuptools python-numpy python-dev libgdal-dev python-gdal swig git g++ libagg-dev libpotrace-dev

GDAL version 2.1.0 or higher is required, as is Potrace v1.14

Then, from this directory (contaning this repo) install the Python requirements and beachfront-py. The use of a virtual environment is recommended.

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt
    (venv) $ pip install .


## Modules & Usage

### Mask

The masking module is used for masking images with vectors (as in the case of a global buffered shoreline), or with a raster mask (such as one derived for clouds in the Landsat BQA band). The two main functions

- mask_with_vector(geoimg, vector, filename=''): Mask a GeoImage with a vector
- create_mask_from_bitmask(geoimg, filename=''): Creates a binary mask from a Landsat quality band to mask out medium and high confidence clouds


```
import gippy
import beachfront.mask as mask

geoimg = gippy.GeoImage('test.tif')
imgout = mask.mask_with_vector(geoimg, ('myshapemask.shp', 'myshapemasklayer'), filename='test-masked.tif')

geoimg = gippy.GeoImage('landsatscene_BQA.TIF')
maskimg = mask.create_mask_from_bitmask(geoimg, filename='cloud-mask.tif')

```

### Process

The process module currently contains one function, calculating the otsu threshold of a raster image, but future general processing functions may be added in the future. 

- otsu_threshold(georaster): Calculates the optimal threshold of an image with a bimodal histogram

```
import gippy
from beachfront.process import otsu_threshold

# open an image assumed to be bimodal
geoimg = gippy.GeoImage(filename)

# calculate threshold on first band of image
threshold = otsu_threshold(geoimg[0])
print(threshold)

# print stats on image: min, max, mean, stddev
print geoimg[0].stats()

```


### Vectorize

The vectorize module supplies functions for tracing a binary imagery that may have nodata values, and converting to geo-located or lat-lon coordinates. The main way to use the vectorize module is on a Gippy GeoRaster, which is a band of a GeoImage.  The potrace() function will use potrace to trace the polygon (aka white, foreground) as a linestring, and convert it to lat-lon coordinates, or geo-located coordinates if desired.

- potrace(geoimg, geoloc=False, close=5.0, minsize=10.0): Traces linestrings along boundaries in a binary image using the Potrace library. Returns array of line coordinates.
- save_geojson(lines, fout) and save_shapefile(lines, fout): Save the lines to a file. Note that the save_shapefile currently assumes the lines are in lat-lon.

#### trace parameters

- geoloc (False): If True, then the coordinates returned will be geo-located in the same projection as the input raster. Otherwise the returned coordinates will be in lat-lon (recommended).
- close (5): Linestrings will be closed if their two endpoints are within this number of pixels. The default is 5, and setting it to 0 will turn it off.
- minsize (10): The minimum size a linestring should be before being filtered out. This corresponds to the potrace parameter 'turdsize', and is not the length of the line but rather some measure of the extent of it. The default of 10 will not filter out many lines. For Landsat, a value of 10000 works well and removing false coasts, but may also remove islands or smaller incomplete shorelines.


```
import gippy
from beachfront.vectorize import potrace
from beachfront.vectorize import save_geojson, save_shapefile

geoimg = gippy.GeoImage(filename)
lines = potrace(geoimg[0], minsize=10000)

save_geojson(lines, fout='my.geojson')
save_shapefile(lines, fout='my.shp')
```


### Logger

The logger module creates a logger streamed to stdout that supports additional keywords for audit logging for the Beachfront project. The logger module will automatically be initialized and used whenever any part of beachfront-py is imported. The quiet the logger, use the mute_logger function.

```
from beachfront.vectorize import potrace
from beachfront.logger import mute_logger

mute_logger()
```


## Development

### Branches
The 'develop' branch is the default branch and contains the latest accepted changes to the code base. Changes should be created in a branch and Pull Requests issues to the 'develop' branch. Releases (anything with a version number) should issue a PR to 'master', then tagged with the proper version using `git tag`. Thus, the 'master' branch will always contain the latest tagged release.

### Testing
Python nose is used for testing, and any new function added to the main library should have at least one corresponding test in the appropriate module test file in the tests/ directory.

### Docker
A Dockerfile and a docker-compose.yml are included for ease of development. The built docker image provides all the system dependencies needed to run the library. The library can also be tested locally, but all system dependencies must be installed first, and the use of a virtualenv is recommended.

To build the docker image use the included docker-compose tasks:

    $ docker-compose build

Which will build an image called 'beachfront-py'. Then the image can be run:

    # this will run the image in interactive mode (open bash script)
    $ docker-compose run bash

    # this willl run the tests using the locally available image
    $ docker-compose run test


## License

Copyright 2016, RadiantBlue Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.