#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The obspy.io.gcf.core test suite.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import os
import unittest

from obspy import read
from obspy.core.utcdatetime import UTCDateTime
from obspy.io.gcf.core import _read_gcf


class CoreTestCase(unittest.TestCase):
    """
    Test cases for gcf core interface
    """
    def setUp(self):
        # directory where the test files are located
        self.path = os.path.join(os.path.dirname(__file__), 'data')

    def test_read_via_obspy(self):
        """
        Read files via obspy.core.stream.read function.
        """
        filename = os.path.join(self.path, '20160603_1955n.gcf')
        # 1
        st = read(filename)
        st.verify()
        self.assertEqual(len(st), 1)
        self.assertEqual(st[0].stats.starttime,
                         UTCDateTime('2016-06-03T19:55:00.000000Z'))
        self.assertEqual(st[0].stats.endtime,
                         UTCDateTime('2016-06-03T19:55:02.990000Z'))
        self.assertEqual(len(st[0]), 300)
        self.assertAlmostEqual(st[0].stats.sampling_rate, 100.0)
        self.assertEqual(st[0].stats.channel, 'HHN')
        self.assertEqual(st[0].stats.station, '6018')

    def test_read_via_module(self):
        """
        Read files via obspy.io.gcf.core._read_gcf function.
        """
        filename = os.path.join(self.path, '20160603_1955n.gcf')
        # 1
        st = _read_gcf(filename)
        st.verify()
        self.assertEqual(len(st), 1)
        self.assertEqual(st[0].stats.starttime,
                         UTCDateTime('2016-06-03T19:55:00.000000Z'))
        self.assertEqual(st[0].stats.endtime,
                         UTCDateTime('2016-06-03T19:55:02.990000Z'))
        self.assertEqual(len(st[0]), 300)
        self.assertAlmostEqual(st[0].stats.sampling_rate, 100.0)
        self.assertEqual(st[0].stats.channel, 'HHN')
        self.assertEqual(st[0].stats.station, '6018')


def suite():
    return unittest.makeSuite(CoreTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
