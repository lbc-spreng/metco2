# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
metco2: A Python package for correcting end-tidal CO2 fluctuations in multi-echo data.
"""

from .due import (due, Doi)

from .info import (
    __version__,
    __author__,
    __copyright__,
    __credits__,
    __license__,
    __maintainer__,
    __email__,
    __status__,
    __url__,
    __packagename__,
    __description__,
    __longdesc__
)

import warnings

# cmp is not used, so ignore nipype-generated warnings
warnings.filterwarnings('ignore', r'cmp not installed')

# Citation for the algorithm.
due.cite(Doi('10.1016/j.neuroimage.2009.05.012'),
         description='Introduces cardiac, respiratory response functions.',
         version=__version__, path='tedana', cite_module=True)
