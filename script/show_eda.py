#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 13:37:06 2019

@author: jan
"""

import numpy as np
from matplotlib import pyplot as plt
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


if __name__ == '__main__':
    fname = "../../Daten/BekJan/HOAF_16.vhdr"
    data, times, _ = load_eda(fname)
    plt.plot(times, data)
    plt.show()
    

