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


def find_blocks(ann, delta=1.5):
    """
    TODO
    """
    mask = ann.description == RESPONSE
    s0 = np.argmax(mask)
    t2 = len(ann) - np.argmax(np.flipud(mask)) - 1

    response_times = ann.onset[mask]
    a, b = np.where(np.diff(response_times) > delta)[0]
    t0 = np.where(mask)[0][a]
    s1 = np.where(mask)[0][a + 1]
    t1 = np.where(mask)[0][b]
    s2 = np.where(mask)[0][b + 1]
    return [[s0, t0], [s1, t1], [s2, t2]]


if __name__ == '__main__':
    fname = "../../Daten/BekJan/HOAF_05.vhdr"
    data, times, raw = load_vhdr(fname)
    ann = raw.annotations

    blocks = np.array(find_blocks(ann))
    print(blocks)
    print(blocks.ravel())
    print(ann.onset[blocks.ravel()])

    raw.plot()
    plt.show()
    
    if False:
        plot_block_hist(ann)
        plt.show()
    
