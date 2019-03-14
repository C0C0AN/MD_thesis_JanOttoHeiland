#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 13:37:06 2019

@author: jan
"""

import mne
import os.path as op
import numpy as np
from matplotlib import pyplot as plt
import shutil
#%matplotlib
from mne.io import read_raw_brainvision
from resp import fix_ch_bug
from numpy.testing import assert_array_equal
import os
import numpy as np
from resp import raw_vhdr


def load_eda(fname, verbose=True):
    """
    Return arrays data, times, and raw.
    """
    raw = raw_vhdr(fname, verbose)
    raw.pick_channels([raw.ch_names[0]])
    data, times = raw[:]
    return data[0], times, raw


file = "../../Daten/BekJan/HOAF_16.vhdr"
raw = read_raw_brainvision(file, preload=True)

# Laden der roh Daten, hier noch in mehreren Dimensionen
data = raw.get_data()

#Definiere dass nur der respiratorische Channel gnutzt wird
raw.pick_channels(['GSR_MR_100'])

fig = raw.plot(None, 10.0,0.0,3,'w',None,(0.8,0.8,0.8),'cyan','auto')

ch_labels = ['GSR_MR_100', 'Resp', 'Stim']
ch_types = ['misc', 'misc', 'stim']
sfreq = 250


