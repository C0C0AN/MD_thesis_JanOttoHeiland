#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 13:37:06 2019

@author: jan
"""
from matplotlib import pyplot as plt
from resp import raw_vhdr
from os import path


def reduce_mean(a, size=1000):
    rest = len(a) % size
    if rest != 0:
        a = a[:-rest]   # elemente abschneiden, sodass len(a) Vielfaches von size
    a = a.reshape(-1, size)
    return a.mean(axis=1)


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
    s=5000;
    plt.title(path.basename(fname) + ", s=" + str(s))
    plt.plot(reduce_mean(times, size=s), reduce_mean(data, size=s))
    plt.show()