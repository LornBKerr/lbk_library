#! /bin/bash

# ##############################################################
# Build a PyPi distribution package for the lbk_library package.
#
# File:       load_to_pypi.sh
# Author:     Lorn B Kerr
# Copyright:  (c) 2022 Lorn B Kerr
# License:    MIT, see file License
# ##############################################################

# Got to directory and start virtual enviroment
cd ~/development/lbk_library
source ~/development/lbk_library/.venv/bin/activate

# remove old distribution files
if [[ -d ./build ]]
then
    rm -rfdv ./build
fi
if [[ -d ./dist ]]
then
    rm -rfdv ./dist
fi
if [[ -d ./src/lbk_library.egg-info ]]
then
    rm -rfdv ./src//lbk_library.egg-info
fi

# load required files to venv
pip install wheel twine

# build library distribution
python -m build

# upload to test.pypi.org
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

