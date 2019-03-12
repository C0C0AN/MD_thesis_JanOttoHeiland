#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:45:01 2019

@author: jan
"""

from blocks import load_blocks
import mne 
from af_in_blocks import af_blocks
from os import path
import matplotlib.pyplot as plt
import glob

df = load_blocks()
fname = "../../Daten/BekJan/HOAF_03.vhdr"   
s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
freq, point = af_blocks(fname, start=s0, endzeit=t0)

%matplotlib
plt.plot(point, freq)
plt.xlabel('Zeit(s)')
plt.ylabel('Af [1/120s')
plt.title("Af Stressblock 1")

def peaks_in_block(fname):
    df = load_blocks()
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    freq, point = af_blocks(fname, start=s0, endzeit=t0)
    fname = "../../Daten/BekJan/"
    endzeit = t0
    return freq, point


for filepath in glob.iglob('../../Daten/BekJan/*.vhdr'):
    print(filepath)
    for i in peaks_in_block('../../Daten/BekJan/'):
        print(i)

plt.plot(point, 20+np.array(freq))
#

#
#fig, ax = plt.subplots()
#ax.plot(y, label='stress_2')
#ax.plot(x, label='stress_1')
#
#plt.xlabel('Zeit(s)')
#plt.ylabel('Puls(bpm)')
#
#plt.title("Pulsdaten Stressblock 1+2")
#
#plt.legend()
#plt.gca().axvspan(0,177.72852, facecolor='0.8',alpha = 0.5)
#plt.gca().axvspan(353.2768,529.1018, facecolor='0.8',alpha = 0.5)

if __name__ == '__main__':
    process_all = True
    if process_all:
        list_blocks = []
        for filepath in glob.iglob('../../Daten/BekJan/*.vhdr'):
            ls.append(peaks_in_block(filepath))
            plt.plot(point,freq)
            print(ls)
        plt.show()
        
    else:
        load_blocks("../../Daten/BekJan/HOAF_13.vhdr")
    

