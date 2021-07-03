# -*- coding: utf-8 -*
"""
Setup script for :mod:`jinja2_ext_outputfile`.

USAGE:
    python setup.py install
"""

import sys
import os.path

HERE0 = os.path.dirname(__file__) or os.curdir
os.chdir(HERE0)
HERE = os.curdir
sys.path.insert(0, HERE)

from setuptools import find_packages, setup


# -----------------------------------------------------------------------------
# CONFIGURATION:
# -----------------------------------------------------------------------------
python_version = sys.version_info[:2]
THIS_PACKAGE = os.path.join(HERE, "jinja2_ext_outputfile")
README = os.path.join(HERE, "README.rst")
description = "".join(open(README).readlines()[4:])


# -----------------------------------------------------------------------------
# UTILITY:
# -----------------------------------------------------------------------------
def find_packages_by_root_package(where):
    """
    Better than excluding everything that is not needed,
    collect only what is needed.
    """
    root_package = os.path.basename(where)
    packages = [ "%s.%s" % (root_package, sub_package)
                 for sub_package in find_packages(where)]
    packages.insert(0, root_package)
    return packages


# -----------------------------------------------------------------------------
# SETUP:
# -----------------------------------------------------------------------------
setup(
    name="jinja2_ext_outputfile",
    version="1.0.0",
    description="Jinja2 extension to redirect template parts to an output-file",
    long_description=description,
    author="Jens Engel",
    author_email="jenisys@noreply.github.com",
    url="http://github.com/jenisys/jinja2-ext-outputfile",
    download_url= "http://pypi.python.org/pypi/jinja2-ext-outputfile",
    provides = ["jinja2_ext_outputfile"],
    packages = find_packages_by_root_package(THIS_PACKAGE),
    # -- REQUIREMENTS:
    # SUPPORT: python2.7, python3.3 (or higher)
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    install_requires=[
        "Jinja2 >= 2.8",
    ],
    tests_require=[
        "pytest <  5.0; python_version <  '3.0'", # >= 4.2
        "pytest >= 5.0; python_version >= '3.0'",
        "pytest-html >= 1.19.0",
    ],
    # DISABLED: use_2to3= bool(python_version >= 3.0),
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    zip_safe = True,
)
