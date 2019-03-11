"""
Find the Response blocks
"""
from resp import load_vhdr
import matplotlib.pyplot as plt
import numpy as np
from resp import find_vhdrs
import pandas as pd
from os import path


RESPONSE = 'Response/R128'


def plot_block_hist(ann):
    mask = ann.description == RESPONSE
    response_times = ann.onset[mask]
    plt.hist(response_times, cumulative=True, bins=200)


def find_blocks(ann, delta=1.5):
    '''
    hier werden die Start und Endzeitpunkte der drei Blocks gefunden
    '''
    mask = ann.description == RESPONSE
    s0 = np.argmax(mask)
    t_last = len(ann) - np.argmax(np.flipud(mask)) - 1

    response_times = ann.onset[mask]
    crit = np.where(np.diff(response_times) > delta)[0]
    times = [s0]
    for c in crit:
        times.append(np.where(mask)[0][c + 0])
        times.append(np.where(mask)[0][c + 1])
    times.append(t_last)
    return times


def get_blocktimes(fname, delta=1.5, show_raw=False):
    '''
    Methode um eine Liste der End und Startpunkte der Bloecke zu generieren
    '''
    data, times, raw = load_vhdr(fname, verbose=False)
    ann = raw.annotations

    blocks = find_blocks(ann, delta=delta)
    blocks = ann.onset[blocks]
    print(",".join([path.basename(fname)] + map(str, blocks)))
    if False:
        print(blocks)
        print(blocks.ravel())
        print(ann.onset[blocks.ravel()])

    if show_raw:
        raw.plot()
        plt.show()

    if False:
        plot_block_hist(ann)
        plt.show()

    return blocks


'''
Hauptmethode die mir eine Liste von allen Blockzeiten von allen Probanden erstellt
'''
if __name__ == '__main__':
    process_all = True

    if process_all:
        l = []
        for fname in find_vhdrs('../../Daten/BekJan/'):
            b = get_blocktimes(fname)
            l.append(b)
    else:
        
        get_blocktimes("../../Daten/BekJan/HOAF_16.vhdr", show_raw=True)
