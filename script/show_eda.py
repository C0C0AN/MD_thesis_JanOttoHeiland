#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 13:37:06 2019

@author: jan
"""
import pickle
import pandas as pd
from matplotlib import pyplot as plt
from resp import raw_vhdr
from os import path
from blocks import load_blocks
from scipy.stats import zscore


def load_eda(fname, verbose=True):
    """
    Return arrays data, times, and raw.
    """
    raw = raw_vhdr(fname, verbose)
    channel = raw.ch_names[0]
    '''
    Überprüfung, ob wrklich der GSR channel der erste ist
    GSR= Galvanic skin response
    '''
    assert channel.startswith('GSR')
    raw.pick_channels([channel])
    data, times = raw[:]
    return data[0], times, raw


def reduce_mean(a, size=1000):
    '''
    size gibt an wieviele Datenpunkte in einem Datenpunkt zusammen gefasst werden
    Da über 19 Millionen Datenpunkte vorlagen ,a = a.reshape(-1, size) : 
    '''
    rest = len(a) % size
    if rest != 0:
        a = a[:-rest]   # elemente abschneiden, sodass len(a) Vielfaches von size
    a = a.reshape(-1, size)
    return a.mean(axis=1)


def compute_reduced_eda(s, filenames, backup="reduced_eda.pickle"):
    ls = []
    if path.exists(backup):
        with open(backup, "rb") as io:
            return pickle.load(io)
    else:
        rs = 1
        for filepath in filenames:
            data, times, _ = load_eda(filepath)
            ls.append((reduce_mean(times, size=s), reduce_mean(data, size=s)))
        with open(backup, "wb") as io:
            pickle.dump(ls, io)
    return ls


if __name__ == '__main__':
    process_all = True
    if process_all:
        '''
        s kann flexibel angepasst werden jenachdem wieviele Datenpunkte wir darstellen wollen 
        '''
        s = 50000
        rs = 1
        filenames = [path.join('../../Daten/BekJan/', f) 
                     for f in load_blocks().index]

        ls = compute_reduced_eda(s, filenames)
        for (times, data) in ls:
            plt.plot(times, pd.Series(data).rolling(rs).mean())
            plt.title('alle Probanden EDA' + " s=" + str(s) + " rs=" + str(rs))
    else:
        fname = "../../Daten/BekJan/HOAF_16.vhdr"
        data, times, _ = load_eda(fname)
        '''
        Plot bei dem nochmal 1000000 Datenpunkte in einem Daenpunkt zusammen gefasst werden 
        '''
        s = 100000
        print("blub")
        plt.title(path.basename(fname) + "s=" + str(s))
        rdata, rtimes = reduce_mean(times, size=s), reduce_mean(data, size=s)
        plt.plot(rtimes, zscore(rdata))
        # matrix = np.array(ls)
        #dmatrix = pd.DataFrame(matrix)
    plt.show()
        

def test_it():
    fname = "../../Daten/BekJan/HOAF_16.vhdr"
    data, times, _ = load_eda(fname)
    plt.plot(times, data)
    plt.show()
    
#dmatrix.plot(kind='line', subplots=True, grid=True, title="Stressblock 2 peaks",
#         sharex=True, sharey=False, legend=False)
#
#[ax.legend(loc=1) for ax in plt.gcf().axes]   
    

