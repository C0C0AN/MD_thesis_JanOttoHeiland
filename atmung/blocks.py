"""
Find the Response blocks
"""
from resp import load_vhdr
import matplotlib.pyplot as plt
import numpy as np


RESPONSE = 'Response/R128'


def plot_block_hist(ann):
    mask = ann.description == RESPONSE
    response_times = ann.onset[mask]
    plt.hist(response_times, cumulative=True, bins=200)


def find_blocks(ann):
    mask = ann.description == RESPONSE
    s0 = np.argmax(ann.description == r)
    s3 = len(ann) - np.argmax(np.flipud(ann.description == RESPONSE)) - 1

    response_times = ann.onset[mask]
    np.where(np.diff(response_times) > 1.5)[0]
    s1, s2 = np.where(np.diff(response_times) > 1.5)[0]

if __name__ == '__main__':
    fname = "../../Daten/BekJan/HOAF_05.vhdr"
    data, times, raw = load_vhdr(fname)
    ann = raw.annotations
    plot_block_hist(ann)
    plt.show()
    
