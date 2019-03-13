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
#
def peaks_in_block1(fname, dauer=60):
    '''
    Methode um es für einen Probanden auszurechnen, 
    dafür relativen Pfad mit Name des Probanden versehen
    '''
    df = load_blocks()
    fname = "../../Daten/BekJan/"  
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    freq, point = af_blocks(fname, start=s0, endzeit=t0)
    return freq, point - point[0] + 0.5 * dauer

%matplotlib
plt.plot(point, freq)
plt.xlabel('Zeit(s)')
plt.ylabel('Af [1/120s')
plt.title("Af Stressblock 1")

def peaks_in_block(fname, dauer=60):
    df = load_blocks()
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    freq, point = af_blocks(fname, dauer=dauer, start=s2, endzeit=t2)
    point = np.array(point)
    '''
    da wir den moving average betrachten, verlieren wir am Anfang und am Ende 
    Zeit diese Zeit müssen wir wieder hinzurechnen
    '''
    return freq, point - point[0] + 0.5 * dauer


#for filepath in glob.iglob('../../Daten/BekJan/*.vhdr'):
#    print(filepath)
#    for i in peaks_in_block('../../Daten/BekJan/'):
#        print(i)

plt.plot(point, 20+np.array(freq))


if __name__ == '__main__':
    process_all = True
    if process_all:
        ls = []
        point = None
        filenames = [path.join('../../Daten/BekJan/', f) 
                     for f in load_blocks().index]
        for filepath in filenames:
            freq, point = peaks_in_block(filepath)
            ls.append(freq)
            matrix = np.array(ls)
            dmatrix = pd.DataFrame(matrix)

dmatrix.index=df.index           
            
            
            plt.plot(point,freq)
            plt.xlabel('Zeit(s)')
            plt.ylabel('Af 1/120s')
            plt.title("Af Stressblock 2 alle P")
#            plt.gca().axvspan(0,177.72852, facecolor='0.8',alpha = 0.5)
#            plt.gca().axvspan(353.2768,529.1018, facecolor='0.8',alpha = 0.5)
#            plt.gca().axvspan(0,177.72852, facecolor='0.8',alpha = 0.5)
#            plt.gca().axvspan(353.2768,529.1018, facecolor='0.8',alpha = 0.5)
            #print(ls)
        plt.show()
        
    else:
        load_blocks("../../Daten/BekJan/HOAF_19.vhdr")
    

