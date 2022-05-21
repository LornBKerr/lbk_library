#! /bin/bash

# Got to directory and start virtual evnviroment
cd ~/development/lbk_library
source ~/development/lbk_library/.venv/bin/activate

# load required files to venv
pip install wheel twine

# build library distribution
python ./setup.py sdist bdist_wheel

# upload to test.pypi.org
twine upload --repository-url https://test.pypi.org/legacy/ dist/*


# load to github
#???
