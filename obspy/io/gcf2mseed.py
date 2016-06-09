#!/usr/bin/python

# convert GCF files to miniseed
# by Ran Nof @ BSL, 2016
# ran.nof@gmail.com

from gcf.core import _read_gcf as read_gcf
from gcf.core import _is_gcf as is_gcf
from glob import glob,sys
from obspy import Stream
import argparse,textwrap

# set the argument parser
parser = argparse.ArgumentParser(
         formatter_class=argparse.RawDescriptionHelpFormatter,
         description='''Convert Guralpe Compressed Format (GCF) to Miniseed''',
         epilog=textwrap.dedent('''\
             See more details regarding GCF:
             http://www.guralp.com/apps/ok?doc=GCF_Intro
    
             The script only converts data streams
        
             Created by Ran Novitsky Nof @ BSL, 2016'''))
parser.add_argument('-o',metavar='Output_file',type=str,help='Output Miniseed file name.')
parser.add_argument('gcf_file',nargs='+',type=str,help='input file(s) name.')
parser.add_argument('-O',metavar='option',type=str,nargs='*',default=["'MSEED'"],help='''\
                         Options for the obspy write command (default: MSEED.)
                         Example option:
                         -O "format='MSEED'" encoding=11 reclen=512 byteorder=1.
                         Note the " and ' around the format and MSEED values.'''
                    )

def getStream(FileList):
  st = Stream()
  for FileName in FileList:
    if is_gcf(FileName):
  		st += read_gcf(FileName)
  return st 		

def main(filesarg,output,writeArgs):
  st = getStream(filesarg)
  eval("st.write(output,%s)"%','.join(writeArgs))

if __name__=='__main__':
  args = parser.parse_args(sys.argv[1:])
  main(args.gcf_file,args.o,args.O)          

