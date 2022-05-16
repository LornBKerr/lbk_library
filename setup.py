# Setup for lbk_library

from codecs import open
from os import path

from setuptools import find_packages, setup

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="lbk_library",
    version="0.3.2",
    description="A Personal Project Support Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LornBKerr/lbk_library",
    author="Lorn B Kerr",
    author_email="lornburtkerr@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
    ],
    packages=["src/lbk_library"],
    include_package_data=True,
    install_requires=[],
)
