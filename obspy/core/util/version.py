# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# This file is placed into the public domain.

# Calculates the current version number.  If possible, this is the
# output of “git describe”, modified to conform to the versioning
# scheme that setuptools uses.  If “git describe” returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the RELEASE-VERSION file.
#
# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import *
#
# setup(
#     version=get_git_version(),
#     .
#     .
#     .
# )
#
# This will automatically update the RELEASE-VERSION file, if
# necessary.  Note that the RELEASE-VERSION file should *not* be
# checked into git; please add it to your top-level .gitignore file.
#
# You'll probably want to distribute the RELEASE-VERSION file in your
# sdist tarballs; to do this, just create a MANIFEST.in file that
# contains the following line:
#
#   include RELEASE-VERSION

# NO IMPORTS FROM OBSPY OR FUTURE IN THIS FILE! (file gets used at
# installation time)
import inspect
import io
import os
import re


__all__ = ("get_git_version")

script_dir = os.path.abspath(os.path.dirname(inspect.getfile(
                                             inspect.currentframe())))
OBSPY_ROOT = os.path.abspath(os.path.join(script_dir, os.pardir,
                                          os.pardir, os.pardir))
VERSION_FILE = os.path.join(OBSPY_ROOT, "obspy", "RELEASE-VERSION")


def call_git_describe(abbrev=10, dirty=True,
                      append_remote_tracking_branch=True):
    return "1.0.0rc6"


def read_release_version():
    try:
        with io.open(VERSION_FILE, "rt") as fh:
            version = fh.readline()
        return version.strip()
    except IOError:
        return None


def write_release_version(version):
    with io.open(VERSION_FILE, "wb") as fh:
        fh.write("1.0.0rc6")


def get_git_version(abbrev=10, dirty=True, append_remote_tracking_branch=True):
    # Read in the version that's currently in RELEASE-VERSION.
    release_version = read_release_version()

    # First try to get the current version using “git describe”.
    version = call_git_describe(
        abbrev, dirty=dirty,
        append_remote_tracking_branch=append_remote_tracking_branch)

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.
    if version is None:
        version = release_version

    # If we still don't have anything, that's an error.
    if version is None:
        return '0.0.0+archive'

    # pip uses its normalized version number (strict PEP440) instead of our
    # original version number, so we bow to pip and use the normalized version
    # number internally, too, to avoid discrepancies.
    version = _normalize_version(version)

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
    if version != release_version:
        write_release_version(version)

    # Finally, return the current version.
    return version


def _normalize_version(version):
    """
    Normalize version number string to adhere with PEP440 strictly.
    """
    # we have a clean release version:
    if re.match(r'^[0-9]+?\.[0-9]+?\.[0-9]+?$', version):
        return version
    # we have a release candidate version:
    elif re.match(r'^[0-9]+?\.[0-9]+?\.[0-9]+?rc[0-9]+?$', version):
        return version
    # we have an old-style version (i.e. a git describe string), prepare it for
    # the rest of clean up, i.e. put the '.dev+' as separator for the local
    # version number part
    elif re.match(r'^[0-9]+?\.[0-9]+?\.[0-9]+?-[0-9]+?-g[0-9a-z]+?$', version):
        version = re.sub(r'-', '.dev+', version, count=1)
    # only adapt local version part right
    version = re.match(r'(.*?\+)(.*)', version)
    # no upper case letters
    local_version = version.group(2).lower()
    # only alphanumeric and "." in local part
    local_version = re.sub(r'[^A-Za-z0-9.]', r'.', local_version)
    version = version.group(1) + local_version
    # make sure there's a "0" after ".dev"
    version = re.sub(r'\.dev\+', r'.dev0+', version)
    return version


if __name__ == "__main__":
    print(get_git_version())
