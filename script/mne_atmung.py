# coding: utf-8
"""
Werte Atmungskurve aus.
"""
from __future__ import print_function
from matplotlib import pyplot as plt
from mne.preprocessing.peak_finder import peak_finder
from os import path
from resp import load_vhdr
import numpy as np


def plot_test_range(times, a=3000, b=3300):
    """
    Plot the respiration data in the range from a to b (seconds)
    """
    a = np.where(times >= a)[0][0]
    b = np.where(times <= b)[0][-1]
    tresp = resp[a:b]
    thres = default
    tpeak_loc, _ = peak_finder(tresp, thresh=thres, extrema=-1)
    tpeak_times = times[a:b][tpeak_loc]
    plt.vlines(x=tpeak_times, ymin=-1, ymax=1)
    plt.plot(times[a:b], tresp)


def plot_resp(times, peak_times, resp):
    """Plot peaks in respiration curve"""
    plt.vlines(x=peak_times, ymin=-1, ymax=1)
    plt.plot(times, resp)


def process(fname, plot=False, histogram=False):
    print("Loading", fname)
    data, times, raw = load_vhdr(fname)
    datavector = data.reshape(-1)
    threshold = (max(datavector)-min(datavector)) / 30
    print("threshold", threshold)
    print("standard deviation", datavector.std())

    # Einspeisen des Datenvektors in peakfinder 
    peak_loc, peak_mag = peak_finder(datavector,thresh=threshold, extrema=-1)
    peak_times = times[peak_loc]

    plt.figure(path.basename(fname))
    plt.xlabel(u"Intervalllänge")
    plt.hist(np.diff(peak_times), bins=np.linspace(0, 7.5, num=100), 
             label="Verteilung der Atmungsintervalllaengen", density=True)
    if plot:
        plt.figure(path.basename(fname)+ ": resp")
        plot_resp(times, peak_times, datavector)

    if histogram:
        plt.figure(path.basename(fname)+ ": resp distribution")
        plt.hist(datavector, bins=np.linspace(-1.5, 1, num=100), density=True)


if __name__ == '__main__':
    import argparse

    data_dir = path.join(path.dirname(__file__), '..', '..', 'Daten')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('file', help='VHDR Datei, die ausgewertet werden soll',
                   type=str, nargs='?',
                   default=path.join(data_dir, 'BekJan', 'HOAF_EDA_Resp0002.vhdr'))
    p.add_argument('-p', '--plot', action='store_true',
                   help='Plotte die Resp-Kurve')
    p.add_argument('-H', '--histogram', action='store_true',
                   help='Plotte die Verteilung der Resp-Kurve')
    args = p.parse_args()

    process(args.file, plot=args.plot, histogram=args.histogram)
    # plot_test_range()
    plt.show()
