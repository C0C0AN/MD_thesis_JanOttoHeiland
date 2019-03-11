"""
Find the Response blocks
"""
from resp import load_vhdr
import matplotlib.pyplot as plt
import numpy as np
from resp import find_vhdrs
import pandas as pd


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
    t2 = len(ann) - np.argmax(np.flipud(mask)) - 1

    response_times = ann.onset[mask]
    a, b = np.where(np.diff(response_times) > delta)[0]
    t0 = np.where(mask)[0][a]
    s1 = np.where(mask)[0][a + 1]
    t1 = np.where(mask)[0][b]
    s2 = np.where(mask)[0][b + 1]
    return [[s0, t0], [s1, t1], [s2, t2]]



def get_blocktimes(fname):
    '''
    Methode um eine Liste der End und Startpunkte der Blöcke zu generieren 
    '''    
    data, times, raw = load_vhdr(fname)
    ann = raw.annotations

    blocks = np.array(find_blocks(ann))
    if False:
        print(blocks)
        print(blocks.ravel())
        print(ann.onset[blocks.ravel()])
    
    return blocks.ravel().tolist()

    if False:
        raw.plot()
        plt.show()
    
    if False:
        plot_block_hist(ann)
        plt.show()


'''
Hauptmethode die mir eine Liste von allen Blockzeiten von allen Probanden erstellt
'''
if __name__ == '__main__':
    l = []
    for fname in find_vhdrs('../../Daten/BekJan/'):
        b = get_blocktimes(fname)
        l.append(b)

    
   # fname = "../../Daten/BekJan/HOAF_05.vhdr"
    #get_blocktimes(fname)

    
