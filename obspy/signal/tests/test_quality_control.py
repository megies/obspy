# -*- coding: utf-8 -*-
"""
The Quality Control test suite.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import unittest

import numpy as np

import obspy
from obspy.core.util.base import NamedTemporaryFile
from obspy.signal.quality_control import MSEEDMetadata


class QualityControlTestCase(unittest.TestCase):
    """
    Test cases for Quality Control.
    """
    def test_no_files_given(self):
        """
        Tests the raised exception if no file is given.
        """
        mseed_metadata = MSEEDMetadata()

        with self.assertRaises(ValueError) as e:
            mseed_metadata.populate_metadata(files=[])

        self.assertEqual(
            e.exception.args[0],
            "Nothing added - no data within the given temporal constraints "
            "found.")

    def test_gaps_and_overlaps(self):
        """
        Test gaps and overlaps.
        """
        # Create a file. No gap between 1 and 2, 10 second gap between 2 and
        # 3, 5 second overlap between 3 and 4, and another 10 second gap
        # between 4 and 5.
        tr_1 = obspy.Trace(data=np.arange(10, dtype=np.int32),
                           header={"starttime": obspy.UTCDateTime(0)})
        tr_2 = obspy.Trace(data=np.arange(10, dtype=np.int32),
                           header={"starttime": obspy.UTCDateTime(10)})
        tr_3 = obspy.Trace(data=np.arange(10, dtype=np.int32),
                           header={"starttime": obspy.UTCDateTime(30)})
        tr_4 = obspy.Trace(data=np.arange(10, dtype=np.int32),
                           header={"starttime": obspy.UTCDateTime(35)})
        tr_5 = obspy.Trace(data=np.arange(10, dtype=np.int32),
                           header={"starttime": obspy.UTCDateTime(55)})
        st = obspy.Stream(traces=[tr_1, tr_2, tr_3, tr_4, tr_5])

        with NamedTemporaryFile() as tf:
            st.write(tf.name, format="mseed")

            mseed_metadata = MSEEDMetadata()
            mseed_metadata.populate_metadata(files=[tf.name])
            self.assertEqual(mseed_metadata._ms_meta['num_gaps'], 2)
            self.assertEqual(mseed_metadata._ms_meta['num_overlaps'], 1)
            self.assertEqual(mseed_metadata._ms_meta['overlaps_len'], 5.0)
            self.assertEqual(mseed_metadata._ms_meta['gaps_len'], 20.0)
            self.assertEqual(mseed_metadata._ms_meta['percent_availability'],
                             44.0 / 64.0 * 100.0)

            # Same again but this time with start-and end time settings.
            mseed_metadata = MSEEDMetadata()
            mseed_metadata.populate_metadata(
                files=[tf.name], starttime=obspy.UTCDateTime(5),
                endtime=obspy.UTCDateTime(60))
            self.assertEqual(mseed_metadata._ms_meta['num_gaps'], 2)
            self.assertEqual(mseed_metadata._ms_meta['num_overlaps'], 1)
            self.assertEqual(mseed_metadata._ms_meta['overlaps_len'], 5.0)
            self.assertEqual(mseed_metadata._ms_meta['gaps_len'], 20.0)
            self.assertEqual(mseed_metadata._ms_meta['percent_availability'],
                             35.0 / 55.0 * 100.0)

            # Head and tail gaps.
            mseed_metadata = MSEEDMetadata()
            mseed_metadata.populate_metadata(
                    files=[tf.name], starttime=obspy.UTCDateTime(-10),
                    endtime=obspy.UTCDateTime(80))
            self.assertEqual(mseed_metadata._ms_meta['num_gaps'], 4)
            self.assertEqual(mseed_metadata._ms_meta['num_overlaps'], 1)
            self.assertEqual(mseed_metadata._ms_meta['overlaps_len'], 5.0)
            self.assertEqual(mseed_metadata._ms_meta['gaps_len'], 45.0)
            self.assertEqual(mseed_metadata._ms_meta['percent_availability'],
                             45.0 / 90.0 * 100.0)

            # Tail gap must be larger than 1 delta, otherwise it does not
            # count.
            mseed_metadata = MSEEDMetadata()
            mseed_metadata.populate_metadata(files=[tf.name],
                                             endtime=obspy.UTCDateTime(64))
            self.assertEqual(mseed_metadata._ms_meta['num_gaps'], 2)
            self.assertEqual(mseed_metadata._ms_meta['gaps_len'], 20.0)
            self.assertEqual(mseed_metadata._ms_meta['percent_availability'],
                             44.0 / 64.0 * 100.0)
            mseed_metadata = MSEEDMetadata()
            mseed_metadata.populate_metadata(files=[tf.name],
                                             endtime=obspy.UTCDateTime(65))
            self.assertEqual(mseed_metadata._ms_meta['num_gaps'], 2)
            self.assertEqual(mseed_metadata._ms_meta['gaps_len'], 20.0)
            self.assertEqual(mseed_metadata._ms_meta['percent_availability'],
                             45.0 / 65.0 * 100.0)
            mseed_metadata = MSEEDMetadata()
            mseed_metadata.populate_metadata(files=[tf.name],
                                             endtime=obspy.UTCDateTime(66))
            self.assertEqual(mseed_metadata._ms_meta['num_gaps'], 3)
            self.assertEqual(mseed_metadata._ms_meta['gaps_len'], 21.0)
            self.assertEqual(mseed_metadata._ms_meta['percent_availability'],
                             45.0 / 66.0 * 100.0)

    def test_gaps_between_multiple_files(self):
        """
        Test gap counting between multiple files. Simple test but there is
        no effective difference between having multiple files and a single
        one with many Traces as internally it is all parsed to a single
        Stream object.
        """
        with NamedTemporaryFile() as tf1, NamedTemporaryFile() as tf2:
            # Two files, same ids but a gap in-between.
            obspy.Trace(data=np.arange(10, dtype=np.int32),
                        header={"starttime": obspy.UTCDateTime(0)}).write(
                tf1.name, format="mseed")
            obspy.Trace(data=np.arange(10, dtype=np.int32),
                        header={"starttime": obspy.UTCDateTime(100)}).write(
                    tf2.name, format="mseed")
            # Don't calculate statistics on the single segments.
            mseed_metadata = MSEEDMetadata()
            mseed_metadata.populate_metadata([tf1.name, tf2.name], c_seg=False)
            self.assertEqual(mseed_metadata._ms_meta['num_gaps'], 1)
            self.assertNotIn("c_segments", mseed_metadata._ms_meta)

    def test_file_with_no_timing_quality(self):
        """
        Tests timing quality extraction in files with no timing quality.
        """
        with NamedTemporaryFile() as tf1:
            obspy.Trace(data=np.arange(10, dtype=np.int32),
                        header={"starttime": obspy.UTCDateTime(0)}).write(
                    tf1.name, format="mseed")
            mseed_metadata = MSEEDMetadata()
            mseed_metadata.populate_metadata([tf1.name])
            self.assertEqual(mseed_metadata._ms_meta['timing_quality_max'],
                             None)
            self.assertEqual(mseed_metadata._ms_meta['timing_quality_min'],
                             None)
            self.assertEqual(mseed_metadata._ms_meta['timing_quality_mean'],
                             None)


def suite():
    return unittest.makeSuite(QualityControlTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
