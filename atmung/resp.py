"""
Provide access to VHDR/EEG data.
"""
from mne.io import read_raw_brainvision
from shutil import copyfile
import os


def load_vhdr(fname):
    raw = mne.io.read_raw_brainvision(fname, preload=True)
    data = raw.get_data()
    # fig = raw.plot(None, 10.0,0.0,3,'w',None,(0.8,0.8,0.8),'cyan','auto')
    raw.pick_channels(['Resp'])
    data, times = raw[:]
    # TODO: 20218200 = ??
    return data, times, raw
