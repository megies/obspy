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
from subprocess import PIPE, Popen


__all__ = ("get_git_version")

script_dir = os.path.abspath(os.path.dirname(inspect.getfile(
                                             inspect.currentframe())))
OBSPY_ROOT = os.path.abspath(os.path.join(script_dir, os.pardir,
                                          os.pardir, os.pardir))
VERSION_FILE = os.path.join(OBSPY_ROOT, "obspy", "RELEASE-VERSION")


def call_git_describe(abbrev=10, dirty=True,
                      append_remote_tracking_branch=True):
    try:
        p = Popen(['git', 'rev-parse', '--show-toplevel'],
                  cwd=OBSPY_ROOT, stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        path = p.stdout.readline().decode().strip()
        p.stdout.close()
    except OSError:
        return None

    if os.path.normpath(path) != OBSPY_ROOT:
        return None

    command = ['git', 'describe', '--abbrev=%d' % abbrev, '--always', '--tags']
    if dirty:
        command.append("--dirty")
    try:
        p = Popen(command, cwd=OBSPY_ROOT, stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readline().decode().strip()
        p.stdout.close()
    except OSError:
        return None

    remote_tracking_branch = None
    if append_remote_tracking_branch:
        try:
            # find out local alias of remote and name of remote tracking branch
            p = Popen(['git', 'branch', '-vv'],
                      cwd=OBSPY_ROOT, stdout=PIPE, stderr=PIPE)
            p.stderr.close()
            remote_info = [line_.decode().rstrip()
                           for line_ in p.stdout.readlines()]
            p.stdout.close()
            remote_info = [line_ for line_ in remote_info
                           if line_.startswith('*')][0]
            remote_info = re.sub(r".*? \[([^ :]*).*?\] .*", r"\1", remote_info)
            remote, branch = remote_info.split("/")
            # find out real name of remote
            p = Popen(['git', 'remote', '-v'],
                      cwd=OBSPY_ROOT, stdout=PIPE, stderr=PIPE)
            p.stderr.close()
            stdout = [line_.decode().strip() for line_ in p.stdout.readlines()]
            p.stdout.close()
            remote = [line_ for line_ in stdout
                      if line_.startswith(remote)][0].split()[1]
            if remote.startswith("git@github.com:"):
                remote = re.sub(r"git@github.com:(.*?)/.*", r"\1", remote)
            elif remote.startswith("https://github.com/"):
                remote = re.sub(r"https://github.com/(.*?)/.*", r"\1", remote)
            elif remote.startswith("git://github.com"):
                remote = re.sub(r"git://github.com/(.*?)/.*", r"\1", remote)
            else:
                remote = None
            if remote is not None:
                remote_tracking_branch = re.sub(r'[^A-Za-z0-9._-]', r'_',
                                                '%s-%s' % (remote, branch))
        except (IndexError, OSError, ValueError):
            pass

    # (this line prevents official releases)
    # should work again now, see #482 and obspy/obspy@b437f31
    if "-" not in line and "." not in line:
        version = "0.0.0.dev+.g%s" % line
    else:
        parts = line.split('-', 1)
        version = parts[0]
        try:
            version += '.dev+' + parts[1]
            if remote_tracking_branch is not None:
                version += '.' + remote_tracking_branch
        # IndexError means we are at a release version tag cleanly,
        # add nothing additional
        except IndexError:
            pass
    return version


def read_release_version():
    try:
        with io.open(VERSION_FILE, "rt") as fh:
            version = fh.readline()
        return version.strip()
    except IOError:
        return None


def write_release_version(version):
    with io.open(VERSION_FILE, "wb") as fh:
        fh.write(("%s\n" % version).encode('ascii', 'strict'))


def get_git_version(abbrev=10, dirty=True, append_remote_tracking_branch=True):
    return "0.10.1"


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
