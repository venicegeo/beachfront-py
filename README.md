# bf-py

bf-py is a library of functions used in the creation of shoreline extraction algorithms for the Beachfront project.

## Installation
There are several system libraries as well pip installable modules. Install scripts are provided in the install directory. Call them from this directory:

    $ install/centos.sh

The script will install all system and python depdencies, and then run all tests in test/.


## Modules


### Mask

The masking module is used for masking images with vectors (as in the case of a global buffered shoreline), or with a raster mask (such as one derived for clouds in the Landsat BQA band).


```
import gippy
from beachfront.mask import open_vector

# get a WFS layer
ds, layer = open_vector(url, layername)

# or, open a shapefile
ds, layer = open_shapefile()

# open an image assumed to be bimodal
geoimg = gippy.GeoImage(filename)

# calculate threshold on first band of image
threshold = otsu_threshold(geoimg[0])
print(threshold)

```


### Process

The process module currently contains one function, calculating the otsu threshold of a raster image, but future general processing functions may be added in the future. 


```
import gippy
from beachfront.process import otsh_threshold

# open an image assumed to be bimodal
geoimg = gippy.GeoImage(filename)

# calculate threshold on first band of image
threshold = otsu_threshold(geoimg[0])
print(threshold)

# print stats on image: min, max, mean, stddev
print geoimg[0].stats()

```


### Vectorize

The vectorize module supplies functions for tracing a binary imagery that may have nodata values, and converting to geo-located or lat-lon coordinates. 

The main way to use the vectorize module is on a Gippy GeoRaster, which is a band of a GeoImage.  The potrace() function will use potrace to trace the polygon (aka white, foreground) as a linestring, and convert it to lat-lon coordinates, or geo-located coordinates if desired.

```
import gippy
from beachfront.vectorize import potrace

geoimg = gippy.GeoImage(filename)
lines = potrace(geoimg[0], geoloc=*[True,False]*)
```

If geoloc is True, then the coordinates returned will be geo-located in the same projection as the input raster. Otherwise the returned coordinates will be in lat-lon.

The save_geojson() and save_shapefile() functions can be used to save the lines to a file. Note that the save_shapefile currently assumes the lines are in lat-lon.

```
from beachfront.vectorize import save_geojson, save_shapefile

save_geojson(lines, fout='my.geojson', source='mydatasource')
save_shapefile(lines, fout='my.shp', source='mydatasource')
```

The source will be set as a field in the resulting output and should contain the data source, such as 'landsat8'.


## Development

### Branches
The 'develop' branch is the default branch and contains the latest accepted changes to the code base. Changes should be created in a branch and Pull Requests issues to the 'develop' branch. Releases (anything with a version number) should issue a PR to 'master', then tagged with the proper version using `git tag`. Thus, the 'master' branch will always contain the latest tagged release.

### Testing
Python nose is used for testing, and any new function added to the main library should have at least one corresponding test in the appropriate module test file in the tests/ directory.

### Docker
A Dockerfile and a docker-compose.yml are included for ease of development. The built docker image provides all the system dependencies needed to run the library. The library can also be tested locally, but all system dependencies must be installed first, and the use of a virtualenv is recommended.

To build the docker image use the included docker-compose tasks:

    $ docker-compose build

Which will build an image called 'bf-py'. Then the imgae can be run:

    # this will run the image in interactive mode (open bash script)
    $ docker-compose run bash

    # this willl run the tests using the locally available image
    $ docker-compose run test
