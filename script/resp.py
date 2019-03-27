"""
Provide access to VHDR/EEG data.
"""
from mne.io import read_raw_brainvision
from glob import glob
from os import path
import shutil
import re
from scipy import signal
from scipy.signal import lfilter

def fix_ch_bug(ifname, ofname, max_ch_len=11):
    """
    Read file at `ifname`, replace `ch_correct` to `ch_wrong` and write that to `ofname`
    """
    with open(ifname) as io:
        v = io.read()
    m = re.search(r'Ch1=(.+?),', v)
    if m:
        ch1 = m.group(1)
        if len(ch1) > max_ch_len:
            new_ch1 = ch1[:max_ch_len]
            v = v.replace(ch1 + ",", new_ch1 + ",")
            v = v.replace(ch1, new_ch1 + " ")
    with open(ofname, "w") as io:
        io.write(v)


def raw_vhdr(fname, verbose=True):
    try:
        backup_fname = fname + ".backup"
        shutil.copyfile(fname, backup_fname)
        fix_ch_bug(fname, fname)
        raw = read_raw_brainvision(fname, preload=True, stim_channel=False, 
                                   verbose=verbose)
        return raw
    finally:
        shutil.move(backup_fname, fname)


def load_vhdr(fname, verbose=True):
    """
    Return arrays data, times, and raw.
    """
    rs=10000
    raw = raw_vhdr(fname, verbose=verbose)
    data = raw.get_data()
    raw.pick_channels(['Resp'])
    data, times = raw[:]
    data=signal.detrend(data, axis=-1, type='linear')
    return data, times, raw


def find_vhdrs(directory):
    """Return a list of all files *.vhdr in `directory`"""
    return sorted(glob(path.join(directory, '*.vhdr')))


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        for f in find_vhdrs(sys.argv[1]):
            print(f)
    else:
        #assert len(sys.argv) >= 3
        fix_ch_bug(sys.argv[1], sys.argv[2])
