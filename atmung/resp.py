"""
Provide access to VHDR/EEG data.
"""
from mne.io import read_raw_brainvision
from glob import glob
from os import path
import shutil


def fix_ch_bug(ifname, ofname, ch_correct="GSR_MR_50_xx", ch_wrong="GSR_MR_50_xx15"):
    """
    Read file at `ifname`, replace `ch_correct` to `ch_wrong` and write that to `ofname`
    """
    with open(ifname) as io:
        v = io.read()
    with open(ofname, "w") as io:
        io.write(v.replace(ch_wrong, ch_correct))


def load_vhdr(fname):
    """
    Return arrays data, times, and raw.
    """
    try:
        backup_fname = fname + ".backup"
        shutil.copyfile(fname, backup_fname)
        fix_ch_bug(fname, fname)
        raw = read_raw_brainvision(fname, preload=True)
    finally:
        shutil.move(backup_fname, fname)

    data = raw.get_data()
    raw.pick_channels(['Resp'])
    data, times = raw[:]
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
        assert len(sys.argv) >= 3
        fix_ch_bug(sys.argv[1], sys.argv[2])
