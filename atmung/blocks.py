"""
Find the Response blocks
"""
from resp import load_vhdr
import matplotlib.pyplot as plt


def plot_block_hist(raw, r='Response/R128'):
    ann = raw.annotations
    response_times = ann.onset[ann.description == r]
    plt.hist(response_times, cumulative=True, bins=200)


if __name__ == '__main__':
    fname = "../../Daten/BekJan/HOAF_05.vhdr"
    data, times, raw = load_vhdr(fname)
    plot_block_hist(raw)
    plt.show()
    
