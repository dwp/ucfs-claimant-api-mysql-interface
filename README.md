# ucfs-claimant-api-mysql-interface

## AWS lambda to provide an interface with the UCFS Claimant API database.

This repo contains Makefile to fit the standard pattern.
This repo is a base to create new non-Terraform repos, adding the githooks submodule, making the repo ready for use.

After cloning this repo, please run:  
`make bootstrap`


## Testing

There are tox unit tests in the module. To run them, you will need the module tox installed with `pip install tox`, 
then go to the root of the module and simply run `tox` to run all the unit tests.

**You should always ensure they work before making a pull request for your branch.**

**If tox has an issue with Python version you have installed, you can specify such as `tox -e py38`.**