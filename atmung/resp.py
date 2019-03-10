"""
Provide access to VHDR/EEG data.
"""
from mne.io import read_raw_brainvision
from shutil import copyfile
import os


def load_vhdr(fname):
    """
    Return arrays data, times, and raw.
    """
    raw = mne.io.read_raw_brainvision(fname, preload=True)
    data = raw.get_data()
    raw.pick_channels(['Resp'])
    data, times = raw[:]
    return data, times, raw
