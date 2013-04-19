#!/bin/bash
# Automated script to build all packages for all distributions.
# schroot environments have to be set up accordingly beforehand.

GITFORK=obspy
GITTARGET=master
# Process command line arguments
while getopts f:t: opt
do
   case "$opt" in
      f) GITFORK=$OPTARG;;
      t) GITTARGET=$OPTARG;;
   esac
done


BASEDIR=/tmp/python-obspy_buildall
GITDIR=$BASEDIR/git
DEBSCRIPTDIR=$GITDIR/misc/debian
LOG=$BASEDIR/build_all_debs.log

BUILDDIR=/tmp/python-obspy_build
PACKAGEDIR=$BUILDDIR/packages

rm -rf $BASEDIR
mkdir -p $BASEDIR
exec 2>&1 >> $LOG
echo '#############'
echo "#### `date`"

git clone https://github.com/obspy/obspy.git $GITDIR

for DIST in squeeze wheezy lucid natty oneiric precise quantal; do
    for ARCH in i386 amd64; do
        DISTARCH=${DIST}_${ARCH}
        echo "#### $DISTARCH"
        cd $GITDIR
        git clean -fxd
        cd /tmp  # can make problems to enter schroot environment from a folder not present in the schroot
        COMMAND="cd $DEBSCRIPTDIR; ./deb__build_debs.sh -f $GITFORK -t $GITTARGET &>> $LOG"
        if [[ "$DIST" == "quantal" ]]
        then
            COMMAND="export GIT_SSL_NO_VERIFY=true; $COMMAND"
        fi
        SCHROOT_SESSION=$(schroot --begin-session -c $DISTARCH)
        echo "$COMMAND" | schroot --run-session -c "$SCHROOT_SESSION"
        schroot -f --end-session -c "$SCHROOT_SESSION"
        mv $PACKAGEDIR/* $BASEDIR
    done
done
ln $BASEDIR/*.deb $PACKAGEDIR/
