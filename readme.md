# bf-py

bf-py is a library of functions used in the creation of shoreline extraction algorithms for the Beachfront project.

## Modules


### Vectorize

The vectorize module supplies functions for tracing a binary imagery that may have nodata values, and converting to geo-located or lat-lon coordinates. 


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
