#!/usr/bin/python
# reads Guralp Compressed Format (GCF) Files
# By Ran Novitsky Nof @ BSL, 2016
# ran.nof@gmail.com
# Based on Guralpe's GCF reference (GCF-RFC-GCFR, Issue C, 2011-01-05)
# more details available from: http://www.guralp.com/apps/ok?doc=GCF_Intro
# last access: June, 2016

import numpy as np
from obspy import UTCDateTime

SPSD = { # Table 3.1: special sample rates
157: 0.1,
161: 0.125,
162: 0.2,
164: 0.25,
167: 0.5,
171: 400,
174: 500,
176: 1000,
179: 2000,
181: 4000
}
ToffsetsD = { # Table 3.1: Time fractional offset denominator
171: 8.,
174: 2.,
176: 4.,
179: 8.,
181: 16.
}
compressionD = { # Table 3.2: format field to data type
1 : '>i4',
2 : '>i2',
4 : '>i1'   
}
bitsD = { # Table 3.2: format field to data bytes
1 : 4, # 32bits
2 : 2, # 16bits
4 : 1  # 8bits
}

def is_gcf(f):
    'Test if file is GCF by reading at least 1 data block'
    while 1:
        header,data = read(f)
        if len(data): 
            break

def decode36(DATA):
    'Decode base 36 data'
    # http://geophysics.eas.gatech.edu/GTEQ/Scream4.4/Decoding_Base_36_numbers_C.htm
    STR = ''
    while DATA:
        imed = DATA % 36
        if imed > 9:
            imed += 7
        STR = chr(imed + 48) + STR
        DATA = DATA / 36
    return STR

def decodeTime(DATA):
    'Decode time field'
    H = DATA / 3600
    M = (DATA % 3600) / 60
    S = DATA % 60   
    return "%02d:%02d:%02d"%(H,M,S)

def decodeDate(days):
    'Decode date field'
    daycount = [31,28,31,30,31,30,31,31,30,31,30,31]
    def isLeapYear(Year):
        return (Year % 4 == 0) and ((Year % 100 != 0) or (Year % 400 == 0))
    year = 1989
    month = 10  #note that month and day are zero referenced
    # The number of days is referenced from 17 Nov 1989
    days += 16
    # Account for leap years
    if isLeapYear(year):
        daycount[1] = 29
    while days>=daycount[month]:
        days = days - daycount[month]
        year = year + (month + 1) / 12
        month = (month + 1) % 12
        if isLeapYear(year):
            daycount[1] = 29
        else:
            daycount[1] = 28
    return "%4d-%02d-%02d"%(year,month+1,days+1)

def decodeDateTime(data):
    '''Decode date and time field.
    The date code is a 32 bit value specifying the start time of the block.
    Bits 0-16 contain the number of seconds since midnight,
    and bits 17-31 the number of days since 17th November 1989.'''
    DATE = decodeDate(data >> 17)
    TIME = decodeTime(data - (data >> 17 << 17))
    starttime = UTCDateTime(DATE+'T'+TIME)
    return starttime

def readDataBlock(f,skipData=False):
    '''Read one data block from GCF file.
    more details can be found here: 
    http://geophysics.eas.gatech.edu/GTEQ/Scream4.4/GCF_Specification.htm
    f - file object to read from
    if skipData is True, Only header is returned.
    if not a data block (SPS=0) - returns None.
    '''
    # get ID
    ID = f.read(4)
    if ID == '': raise EOFError # got to EOF
    ID = np.frombuffer(ID,count=1,dtype=np.uint32).byteswap()
    if ID >> 31 & 0b1 > 0 :
        ID = (ID << 6) >> 6
    ID = decode36(ID)
    # get Stream ID
    stID = f.read(4)
    stID = np.frombuffer(stID,count=1,dtype=np.uint32).byteswap()
    stID = decode36(stID)
    # get Date & Time
    data = f.read(4)
    data = np.frombuffer(data,count=1,dtype=np.uint32).byteswap()
    DATE = decodeDate(data >> 17)
    TIME = decodeTime(data - (data >> 17 << 17))
    starttime = UTCDateTime(DATE+'T'+TIME)
    # get data format
    data = f.read(4)
    # get reserved, Samples per second, data type compression, number of 32bit records (N)
    reserved,SPS,compress,N = np.frombuffer(data,count=4,dtype=np.uint8)
    compression = compress &  0b00001111 # get compression code
    Toffset = compress >> 4 # get time offset
    if Toffset>0:
        starttime = starttime + Toffset/ToffsetsD[SPS]
    if SPS in SPSD:
        SPS = SPSD[SPS] # get special SPS value if needed
    if not SPS: 
        f.seek(N*4,1) # skip if not a data block
        if 1008-N*4>0: f.seek(1008-N*4,1) # keep skipping to get 1008 record
        return None
    NoS = int(N)*compression # number of samples
    header = {}
    header['starttime'] = starttime
    header['station'] = stID[:4]
    header['channel'] = 'HH'+stID[4].capitalize()
    header['sampling_rate'] = SPS
    if skipData:
        f.seek(4*(N+2),1) # skip data part (inc. FIC and RIC)
        return header
    else:
        # get FIC
        FIC = np.frombuffer(f.read(4),count=1,dtype='>i4')
        # get incremental data 
        data = np.frombuffer(f.read(4*N),count=NoS,dtype=compressionD[compression])
        # construct time series
        data = (FIC + np.cumsum(data)).astype('>i4')
        # get RIC
        RIC = np.frombuffer(f.read(4),count=1,dtype='>i4')
        # skip if not a full record
        if 1000-int(N)*4 > 0:
            f.seek(1000-int(N)*4,1)
        # verify last data sample matches RIC
        if not data[-1]==RIC:
            raise ValueError("Last sample mismatch with RIC")
        return header,data

def read_header(f):
    'Reads header only from GCF file.'
    return readDataBlock(f,skipData=True)

def read(f):
    'Reads header and data from GCF file.'
    return readDataBlock(f,skipData=False)