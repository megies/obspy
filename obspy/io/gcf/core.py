# -*- coding: utf-8 -*-
"""
GCF bindings to ObsPy core module.
"""

from obspy import Stream, Trace
from . import libgcf


def _is_gcf(filename):
    """
    Checks whether a file is GCF or not.
    :type filename: str
    :param filename: GCF file to be checked.
    :rtype: bool
    :return: ``True`` if a GCF file.
    """
    # Open file.
    try:
        with open(filename, 'rb') as f:
            libgcf.is_gcf(f)
    except:
        return False
    return True


def _read_gcf(filename, headonly=False, **kwargs):  # @UnusedVariable
    """
    Reads a GCF file and returns a Stream object.
    only GCF files containing data records are supported.
    .. warning::
        This function should NOT be called directly, it registers via the
        ObsPy :func:`~obspy.core.stream.read` function, call this instead.
    :type filename: str
    :param filename: GCF file to be read.
    :type headonly: bool, optional
    :param headonly: If True read only head of GCF file.
    :rtype: :class:`~obspy.core.stream.Stream`
    :returns: Stream object containing header and data.
    .. rubric:: Example
    >>> from obspy import read
    >>> st = read("/path/to/filename.gcf")
    """
    traces = []
    with open(filename, 'rb') as f:
        # reading multiple gse2 parts
        while True:
            try:
                if headonly:
                    header = libgcf.read_header(f)
                    if header:
                        traces.append(Trace(header=header))
                else:
                    hd = libgcf.read(f)
                    if hd:
                        traces.append(Trace(header=hd[0], data=hd[1]))
            except EOFError:
                break
    return Stream(traces=traces)
