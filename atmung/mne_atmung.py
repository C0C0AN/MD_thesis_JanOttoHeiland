# coding: utf-8
from __future__ import print_function
from matplotlib import pyplot as plt
from mne.preprocessing.peak_finder import peak_finder
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


def process(fname):
    print("Loading", fname)
    data, times, raw = load_vhdr(fname)
    datavector = data.reshape(-1)
    threshold = (max(datavector)-min(datavector))/30

    # Einspeisen des Datenvektors in peakfinder 
    peak_loc, peak_mag = peak_finder(datavector,thresh=threshold, extrema=-1)
    peak_times = times[peak_loc]
    # resp = raw.get_data()[0]
    plt.xlabel(u"Intervalllänge")
    plt.hist(np.diff(peak_times), bins=np.linspace(0, 7.5, num=100), 
             label="Verteilung der Atmungsintervalllaengen", density=True)


if __name__ == '__main__':
    import sys

    fname = '/home/jan/Documents/Doktorarbeit/Daten/BekJan/HOAF_EDA_Resp0002.vhdr'
    if len(sys.argv) >= 2:
        fname = sys.argv[1]

    process(fname)
    # plot_test_range()
    plt.show()


def _peak_detection():
    start = 1098
    stop = 1822

    def number_peak(start =start, stop=stop):
        return len(peak_times[(peak_times>=start )& (peak_times<=stop)])

    pt_1 = peak_times[(peak_times>=start )& (peak_times<=stop)]

    len(pt_1)


def _tests():
    times[20120541]
    # In[30]:
    # min(datavector)
    # # In[31]:
    # max(datavector)
    # # In[32]:
    # number_peak()
    # # In[49]:

