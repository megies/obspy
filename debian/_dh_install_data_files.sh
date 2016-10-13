#!/bin/sh

for TESTSDIR in `find . -type d -regextype posix-egrep -regex './debian/tmp/usr/lib/python2.7/dist-packages/obspy/.*/tests/(data|images)'`
do
    SUFFIX=`echo $TESTSDIR | sed 's#.*-packages/##'`
    TARGET=usr/share/${SUFFIX}
    dh_installdirs -p python-obspy-dbg ${TARGET}
    dh_install -p python-obspy-dbg ${TESTSDIR}/* ${TARGET}
done
dh_installdirs -p python-obspy-dbg usr/share/obspy/io/mseed/tests/data/libmseed
dh_install -p python-obspy-dbg ./debian/tmp/usr/lib/python2.7/dist-packages/obspy/io/mseed/src/libmseed/test/*.ref usr/share/obspy/io/mseed/tests/data/libmseed
dh_install -p python-obspy-dbg ./debian/tmp/usr/lib/python2.7/dist-packages/obspy/io/mseed/src/libmseed/test/*.test usr/share/obspy/io/mseed/tests/data/libmseed
