# -*- coding: utf-8 -*-
"""
obspy.io.gcf - Guralp Compressed Format read support for ObsPy
==============================================================
This module provides read support for GCF waveform data and header info.
Most methods are based on info from Guralp site
http://geophysics.eas.gatech.edu/GTEQ/Scream4.4/GCF_Specification.htm

:copyright:
    The ObsPy Development Team (devs@obspy.org) & Ran Novitsky Nof
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
Reading
-------
Similar to reading any other waveform data format using :mod:`obspy.core`:
>>> from obspy import read
>>> st = read("/path/to/datafile.gcf")
The format will be determined automatically.

Writing
-------
You may export the data to the file system using the
:meth:`~obspy.core.stream.Stream.write` method of an existing
:class:`~obspy.core.stream.Stream` object
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
