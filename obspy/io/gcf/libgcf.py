# -*- coding: utf-8 -*-
# reads Guralp Compressed Format (GCF) Files
# By Ran Novitsky Nof @ BSL, 2016
# ran.nof@gmail.com
# Based on Guralp's GCF reference (GCF-RFC-GCFR, Issue C, 2011-01-05)
# more details available from: http://www.guralp.com/apps/ok?doc=GCF_Intro
# last access: June, 2016
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import numpy as np

from obspy import UTCDateTime

sps_d = {  # Table 3.1: special sample rates
    157: 0.1,
    161: 0.125,
    162: 0.2,
    164: 0.25,
    167: 0.5,
    171: 400,
    174: 500,
    176: 1000,
    179: 2000,
    181: 4000}
time_offsets_d = {  # Table 3.1: Time fractional offset denominator
    171: 8.,
    174: 2.,
    176: 4.,
    179: 8.,
    181: 16.}
compression_d = {  # Table 3.2: format field to data type
    1: '>i4',
    2: '>i2',
    4: '>i1'}
bits_d = {  # Table 3.2: format field to data bytes
    1: 4,  # 32bits
    2: 2,  # 16bits
    4: 1}   # 8bits


def is_gcf(f):
    'Test if file is GCF by reading at least 1 data block'
    header, data = read_data_block(f)


def decode36(data):
    'Decode base 36 data'
    # http://geophysics.eas.gatech.edu/GTEQ/Scream4.4/Decoding_Base_36_numbers_C.htm
    s = ''
    while data:
        imed = data % 36
        if imed > 9:
            imed += 7
        s = chr(imed + 48) + s
        data = data / 36
    return s


def decode_date_time(data):
    '''Decode date and time field.
    The date code is a 32 bit value specifying the start time of the block.
    Bits 0-16 contain the number of seconds since midnight,
    and bits 17-31 the number of days since 17th November 1989.'''
    days = data >> 17
    secs = data & 0x1FFFF
    starttime = UTCDateTime('1989-11-17') + days * 86400 + secs
    return starttime


def read_data_block(f, headonly=False, channel_prefix="HH", **kwargs):
    '''Read one data block from GCF file.
    more details can be found here:
    http://geophysics.eas.gatech.edu/GTEQ/Scream4.4/GCF_Specification.htm
    f - file object to read from
    if skipData is True, Only header is returned.
    if not a data block (SPS=0) - returns None.
    '''
    # get ID
    sysid = np.fromfile(f, count=1, dtype='>u4')
    if not sysid:
        raise EOFError  # got to EOF
    if sysid >> 31 & 0b1 > 0:
        sysid = (sysid << 6) >> 6
    sysid = decode36(sysid)
    # get Stream ID
    stid = np.fromfile(f, count=1, dtype='>u4')
    stid = decode36(stid)
    # get Date & Time
    data = np.fromfile(f, count=1, dtype='>u4')
    starttime = decode_date_time(data)
    # get data format
    # get reserved, SPS, data type compression, number of 32bit records (N)
    reserved, sps, compress, N = np.fromfile(f, count=4, dtype='>u1')
    compression = compress & 0b00001111  # get compression code
    t_offset = compress >> 4  # get time offset
    if t_offset > 0:
        starttime = starttime + t_offset / time_offsets_d[sps]
    if sps in sps_d:
        sps = sps_d[sps]  # get special SPS value if needed
    if not sps:
        f.seek(N * 4, 1)  # skip if not a data block
        if 1008 - N * 4 > 0:
            f.seek(1008 - N * 4, 1)  # keep skipping to get 1008 record
        return None
    npts = int(N) * compression  # number of samples
    header = {}
    header['starttime'] = starttime
    header['station'] = stid[:4]
    header['channel'] = (channel_prefix[:2] + stid[4]).upper()
    header['sampling_rate'] = sps
    header['npts'] = npts
    if headonly:
        f.seek(4 * (N + 2), 1)  # skip data part (inc. FIC and RIC)
        # skip to end of block if only partly filled with data
        if 1000 - int(N) * 4 > 0:
            f.seek(1000 - int(N) * 4, 1)
        return header
    else:
        # get FIC
        fic = np.fromfile(f, count=1, dtype='>i4')
        # get incremental data
        data = np.fromfile(f, count=npts,
                           dtype=compression_d[compression])
        # construct time series
        data = (fic + np.cumsum(data)).astype('>i4')
        # get RIC
        ric = np.fromfile(f, count=1, dtype='>i4')
        # skip to end of block if only partly filled with data
        if 1000 - int(N) * 4 > 0:
            f.seek(1000 - int(N) * 4, 1)
        # verify last data sample matches RIC
        if not data[-1] == ric:
            raise ValueError("Last sample mismatch with RIC")
        return header, data


def read_header(f, **kwargs):
    'Reads header only from GCF file.'
    return read_data_block(f, headonly=True, **kwargs)


def read(f, **kwargs):
    'Reads header and data from GCF file.'
    return read_data_block(f, headonly=False, **kwargs)