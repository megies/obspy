#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to create new models.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import glob
import inspect
import os
from math import pi

from obspy.taup.slowness_model import SlownessModel
from obspy.taup.tau_model import TauModel
from obspy.taup.velocity_model import VelocityModel

# Most generic way to get the data directory.
__DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe()))), "data")


class TauP_Create(object):
    """
    TauP_Create - Re-implementation of the seismic travel time
    calculation method described in "The Computation of Seismic Travel
    Times" by Buland and Chapman, BSSA vol. 73, No. 5, October 1983,
    pp 1271-1302. This creates the SlownessModel and tau branches and
    saves them for later use.
    """
    def __init__(self, input_filename, output_filename, verbose=False,
                 min_delta_p=0.1, max_delta_p=11.0, max_depth_interval=115.0,
                 max_range_interval=2.5, max_interp_error=0.05,
                 allow_inner_core_s=True):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.debug = verbose
        self.min_delta_p = min_delta_p
        self.max_delta_p = max_delta_p
        self.max_depth_interval = max_depth_interval
        self.max_range_interval = max_range_interval
        self.max_interp_error = max_interp_error
        self.allow_inner_core_s = allow_inner_core_s

    def loadVMod(self):
        """ Tries to load a velocity model via readVelocityFile from the
        directory specified on command line, or from ./data/.
        """
        # Read the velocity model file.
        filename = self.input_filename
        if self.debug:
            print("filename =", filename)
        self.vMod = VelocityModel.readVelocityFile(filename)
        if self.vMod is None:
            # try and load internally
            # self.vMod = TauModelLoader.loadVelocityModel(self.model_filename)
            # Frankly, I don't think it's a good idea to somehow load the
            # model from a non-obvious path. Better to just raise the
            # exception and force user to be clear about what VelocityModel
            # to read from where. Maybe this could be done sensibly,
            # as in if a model is specified but no path, some standard models
            # can be used?
            pass
        if self.vMod is None:
            raise IOError("Velocity model file not found: " + filename)
        # If model was read:
        if self.debug:
            print("Done reading velocity model.")
            print("Radius of model " + self.vMod.modelName + " is " +
                  str(self.vMod.radiusOfEarth))
        # if self.debug:
        #    print("velocity mode: " + self.vMod)
        return self.vMod

    def createTauModel(self, vMod):
        """ Takes a velocity model and makes a slowness model out of it,
        then passes that to TauModel. """
        if vMod is None:
            raise ValueError("vMod is None.")
        if vMod.isSpherical is False:
            raise Exception("Flat slowness model not yet implemented.")
        SlownessModel.DEBUG = self.debug
        if self.debug:
            print("Using parameters provided in TauP_config.ini (or defaults "
                  "if not) to call SlownessModel...")

        self.sMod = SlownessModel(
            vMod, self.min_delta_p, self.max_delta_p, self.max_depth_interval,
            self.max_range_interval * pi / 180.0, self.max_interp_error,
            self.allow_inner_core_s,
            SlownessModel.DEFAULT_SLOWNESS_TOLERANCE)
        if self.debug:
            print("Parameters are:")
            print("taup.create.min_delta_p = " + str(self.sMod.minDeltaP) +
                  " sec / radian")
            print("taup.create.maxDeltaP = " + str(self.sMod.maxDeltaP) +
                  " sec / radian")
            print("taup.create.maxDepthInterval = " +
                  str(self.sMod.maxDepthInterval) + " kilometers")
            print("taup.create.maxRangeInterval = " +
                  str(self.sMod.maxRangeInterval) + " degrees")
            print("taup.create.maxInterpError = " +
                  str(self.sMod.maxInterpError) + " seconds")
            print("taup.create.allowInnerCoreS = " +
                  str(self.sMod.allowInnerCoreS))
            print("Slow model " + " " + str(self.sMod.getNumLayers(True)) +
                  " P layers," + str(self.sMod.getNumLayers(False)) +
                  " S layers")
        # if self.debug:
        #    print(self.sMod)
        # set the debug flags to value given here:
        TauModel.DEBUG = self.debug
        SlownessModel.DEBUG = self.debug
        # Creates tau model from slownesses.
        return TauModel(self.sMod)

    def run(self):
        """ Creates a tau model from a velocity model. Called by
        TauP_Create.main after loadVMod; calls createTauModel and
        writes the result to a .taup file in ./data/taup_models/ (if not
        specified differently).
        """
        try:
            self.tMod = self.createTauModel(self.vMod)
            # this reassigns model! Used to be TauModel() class,
            # now it's an instance of it.
            if self.debug:
                print("Done calculating Tau branches.")

            if not os.path.exists(os.path.dirname(self.output_filename)):
                os.makedirs(os.path.dirname(self.output_filename))
            self.tMod.serialize(self.output_filename)
            if self.debug:
                print("Done Saving " + self.output_filename)
        except IOError as e:
            print("Tried to write!\n Caught IOError. Do you have write "
                  "permission in this directory?", e)
        except KeyError as e:
            print('file not found or wrong key?', e)
        finally:
            if self.debug:
                print("Method run is done, but not necessarily successful.")


def get_builtin_models():
    """
    Get a list of names of builtin models in obspy/taup/data folder that can be
    loaded by only specifying the model name (filename without '.npz'
    extension).
    """
    return glob.glob(os.path.join(__DATA_DIR, "*.npz"))


def get_builtin_tvel_files():
    """
    Get a list of paths to builtin '.tvel' files in obspy/taup/data folder that
    can be used to build models from.
    """
    return glob.glob(os.path.join(__DATA_DIR, "*.tvel"))


def build_taup_model(tvel_filename, output_folder=None):
    """
    Builds a :class:`~obspy.taup.tau_model.TauModel` from the specified "tvel"
    file and saves it in ObsPy's own format, which can be loaded using
    :meth:`~obspy.taup.tau_model.TauModel.from_file`. The output file will have
    the same name as the input with '.npz' as file extension.

    :type tvel_filename: str
    :param tvel_filename: Absolute path of input tvel file.
    :type output_folder: str
    :param output_folder: Directory in which the built
        :class:`~obspy.taup.tau_model.TauModel` will be stored. Defaults to
        directory of input file.
    """
    if output_folder is None:
        output_folder = __DATA_DIR

    model_name = os.path.splitext(os.path.basename(tvel_filename))[0]
    output_filename = os.path.join(output_folder, model_name + ".npz")

    print("Building obspy.taup model for '%s' ..." % tvel_filename)
    mod_create = TauP_Create(input_filename=tvel_filename,
                             output_filename=output_filename)
    mod_create.loadVMod()
    mod_create.run()


def build_all_taup_models():
    """
    Builds all :class:`~obspy.taup.tau_model.TauModel`s in `obspy/taup/data`
    directory.
    """
    for model in get_builtin_tvel_files():
        build_taup_model(tvel_filename=model)


if __name__ == '__main__':
    build_all_taup_models()
