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
import numpy as np


def peaks_in_block1P(fname="../../Daten/BekJan/HOAF_02.vhdr", dauer=60):
    """
    Methode um es für einen Probanden auszurechnen,
    dafür relativen Pfad mit Name des Probanden versehen
    """
    df = load_blocks()
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    freq, point = af_blocks(fname, dauer=dauer, start=s2, endzeit=t2)
    point = np.array(point)
    # freq, point = af_blocks(fname, start=s0, endzeit=t0)
    """
    Plot der nicht die Datenpunkte sondern noch die Zeiten betrachtet,
    da kein Vergleich zwischen den Blöcken
    """
    point = point - point[0] + 0.5 * dauer
    #%matplotlib
    plt.plot(point, freq)
    plt.xlabel("Zeit(s)")
    plt.ylabel("Af 1/120s")
    plt.title("Af_Stressblock_x")
    plt.gca().axvspan(6, 154, facecolor="0.8", alpha=0.5)
    plt.gca().axvspan(182, 330, facecolor="0.8", alpha=0.5)
    plt.gca().axvspan(358, 506, facecolor="0.8", alpha=0.5)
    plt.gca().axvspan(534, 682, facecolor="0.8", alpha=0.5)
    return freq, point


def peaks_in_block(fname, dauer=60, block0=True):
    """
    aufrufen der Funktion für 1 Stressblock: freq0, point0 = peaks_in_block(fname)
    block0= true, für 2 Stressblock:
    freq2, point2 = peaks_in_block(fname, block0=False), block0 auf false
    plot: plt.plot(point0, freq0)
    plt.plot(point2, freq2)
    """
    df = load_blocks()
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    s, t = (s0, t0) if block0 else (s2, t2)
    freq, point = af_blocks(fname, dauer=dauer, start=s, endzeit=t)
    point = np.array(point)
    """
    da wir den moving average betrachten, verlieren wir am Anfang und am Ende 
    Zeit diese Zeit müssen wir wieder hinzurechnen
    """
    return freq, point - point[0] + 0.5 * dauer


if __name__ == "__main__":
    process_all = True
    if process_all:
        ls = []
        point = None
        filenames = [path.join("../../Daten/BekJan/", f) for f in load_blocks().index]
        for filepath in filenames:
            freq, point = peaks_in_block(filepath)
            ls.append(freq)
            matrix = np.array(ls)
            dmatrix = pd.DataFrame(matrix)

df_peak.columns = [
    "HOAF_01",
    " HOAF_02",
    "HOAF_03",
    "HOAF_04",
    "HOAF_05",
    "HOAF_09",
    "HOAF_11",
    "HOAF_12",
    "HOAF_13",
    "HOAF_14",
    "HOAF_15",
    "HOAF_16",
    "HOAF_17",
    "HOAF_19",
    "HOAF_20",
    "HOAF_21",
    "HOAF_22",
    "HOAF_23",
    "HOAF_24",
    "HOAF_25",
    "HOAF_26",
    "HOAF_27",
    "HOAF_28",
    "HOAF_29",
]
k = pd.DataFrame(dmatrix)
df_peak = k.transpose()

"""
Plot für einzelne Probanden und Kombination 
"""

df_peak.index.names = ["Datenpunkt alle 1,45 sek"]
plt.ylabel("Atemfreq[1/60sek]")
df_peak.plot(x=None, y=[1, 2], title="Af_2_Stressblock")
"""
Plot über alle Probanden
"""
df_peak.plot(
    kind="line", subplots=True, grid=True, sharex=True, sharey=False, fontsize=7
)

[ax.legend(loc=1) for ax in plt.gcf().axes]
plt.xlabel("Datenpunkt alle 1,45 sek", fontsize=15)
plt.ylabel(
    "Atemfreq[1/60sek]", horizontalalignment="right", y=18, labelpad=25, fontsize=15
)
plt.title(
    "Stressblock 2 Atemfrequenz", horizontalalignment="right", x=0.7, y=30, fontsize=40
)
