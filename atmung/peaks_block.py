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
def peaks_in_block1P(fname, dauer=60):
    '''
    Methode um es für einen Probanden auszurechnen, 
    dafür relativen Pfad mit Name des Probanden versehen
    '''
    df = load_blocks()
    fname = "../../Daten/BekJan/"  
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    freq, point = af_blocks(fname, dauer=dauer, start=s2, endzeit=t2)
    point = np.array(point)
    #freq, point = af_blocks(fname, start=s0, endzeit=t0)
    '''
    Plot der nicht die Datenpunkte sondern noch die Zeiten betrachtet,
    da kein Vergleich zwischen den Blöcken
    '''
%matplotlib
plt.plot(point, freq)
plt.xlabel('Zeit(s)')
plt.ylabel('Af 1/120s')
plt.title("Af_Stressblock_x")
plt.gca().axvspan(6,154, facecolor='0.8',alpha = 0.5)
plt.gca().axvspan(182,330, facecolor='0.8',alpha = 0.5)
plt.gca().axvspan(358,506, facecolor='0.8',alpha = 0.5)
plt.gca().axvspan(534,682, facecolor='0.8',alpha = 0.5)
return freq, point - point[0] + 0.5 * dauer

def peaks_in_block(fname, dauer=60):
    df = load_blocks()
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    freq, point = af_blocks(fname, dauer=dauer, start=s0, endzeit=t0)
    point = np.array(point)
    '''
    da wir den moving average betrachten, verlieren wir am Anfang und am Ende 
    Zeit diese Zeit müssen wir wieder hinzurechnen
    '''
    return freq, point - point[0] + 0.5 * dauer

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

  
df_peak = k.transpose()

'''
Plot für einzelne Probanden und Kombination 
'''
df_peak.plot(x=None, y=[1,2], title='Af_2_Stressblock')
df_peak.index.name = 'blocktime'

'''
Plot über alle Probanden
'''
df_peak.plot(kind='line', subplots=True, grid=True, title="Stressblock 2 peaks",
             sharex=True, sharey=False, legend=False)

[ax.legend(loc=1) for ax in plt.gcf().axes]    

  

