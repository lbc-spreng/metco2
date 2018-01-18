# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Base module variables
"""

__version__ = ''
__author__ = 'Elizabeth DuPre'
__copyright__ = 'Copyright 2017, Elizabeth DuPre'
__credits__ = ['Elizabeth DuPre']
__license__ = 'GPL 3.0'
__maintainer__ = 'Elizabeth DuPre'
__email__ = 'emd222@cornell.edu'
__status__ = 'Prototype'
__url__ = 'https://github.com/lbc-spreng/metco2'
__packagename__ = 'metco2'
__description__ = ("End-tidal CO2 correction for multi-echo "
                   "functional magnetic resonance imaging (fMRI) data.")
__longdesc__ = ("To do.")

DOWNLOAD_URL = (
    'https://github.com/lbc-spreng/{name}/archive/{ver}.tar.gz'.format(
        name=__packagename__, ver=__version__))

REQUIRES = [
    'numpy',
    'nipype',
    'pybids>=0.4.0',
    'scipy'
]

LINKS_REQUIRES = [
    'git+https://github.com/rmarkello/peakdet.git'
]

TESTS_REQUIRES = [
    "codecov",
    "pytest",
]

EXTRA_REQUIRES = {
    'doc': ['sphinx>=1.5.3', 'sphinx_rtd_theme', 'sphinx-argparse'],
    'tests': TESTS_REQUIRES,
    'duecredit': ['duecredit'],
}

# Enable a handle to install all extra dependencies at once
EXTRA_REQUIRES['all'] = [val for _, val in list(EXTRA_REQUIRES.items())]

# Package classifiers
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'License :: OSI Approved :: LGPL License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
]
