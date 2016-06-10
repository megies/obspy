#!/usr/bin/python

# convert GCF files to miniseed
# by Ran Nof @ BSL, 2016
# ran.nof@gmail.com

import argparse
import sys
import textwrap

from obspy import Stream
from obspy.io.gcf.core import _is_gcf as is_gcf, _read_gcf as read_gcf


# set the argument parser
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''Convert Guralp Compressed Format (GCF) to Miniseed''',
    epilog=textwrap.dedent('''\
             See more details regarding GCF:
             http://www.guralp.com/apps/ok?doc=GCF_Intro

             The script only converts data streams

             Created by Ran Novitsky Nof @ BSL, 2016'''))
parser.add_argument('-o', '--output_file', type=str,
                    help='Output Miniseed file name.', required=True)
parser.add_argument('gcf_file', nargs='+', type=str,
                    help='input file(s) name.')
parser.add_argument('-O', '--options', type=str, nargs='*',
                    default=["'MSEED'"], help='''
                    Options for the obspy write command (default: MSEED.)
                    Example option:
                    -O "format='MSEED'" encoding=11 reclen=512 byteorder=1.
                    Note the " and ' around the format and MSEED values.'''
                    )


def getstream(filelist):
    st = Stream()
    for filename in filelist:
        if is_gcf(filename):
            st += read_gcf(filename)
    return st


def main(filesarg, output, writeargs):
    st = getstream(filesarg)
    eval("st.write(output,%s)" % ','.join(writeargs))


if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])
    main(args.gcf_file, args.output_file, args.options)
