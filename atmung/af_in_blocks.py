# coding: utf-8
"""
Zählen der Peaks in Blöcken von zum Beispiel Minuten (60sec)
"""
from resp import load_vhdr
from blocks import load_blocks
from matplotlib import pyplot as plt
from mne.preprocessing.peak_finder import peak_finder
from os import path


def number_peaks(peak_times, start, stop):
    return len(peak_times[(peak_times >= start) & (peak_times < stop)])


def af_blocks(fname, dauer=60):
    '''
    return af /min Zeit(xAchse)
    '''
    data, times, raw = load_vhdr(fname)
    datavector = data.reshape(-1)
    threshold = (max(datavector)-min(datavector)) / 30

    peak_loc, peak_mag = peak_finder(datavector,thresh=threshold, extrema=-1)
    peak_times = times[peak_loc]

    endzeit = times[-1]
    start = 0
    stop = dauer
    l = []
    t = []
    while stop <= endzeit:
        t.append(0.5*(start + stop))
        l.append(number_peaks(peak_times, start, stop))
        start = start + dauer
        stop = stop + dauer
    return l, t


def plot_af(l, t):
    plt.plot(t, l, label="Atemfreq")
    plt.xlabel('Zeit(s)')
    plt.ylabel('Atemfreq [1/min]')
    plt.title("peaks in resp curve")


def plot_blocks(fname):
    df = load_blocks()
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    plt.gca().axvspan(s0, t0, facecolor='0.8', alpha = 0.5)
    plt.gca().axvspan(s2, t2, facecolor='0.8', alpha = 0.5)
    plt.legend()


if __name__ == '__main__':
    fname = "../../Daten/BekJan/HOAF_16.vhdr"
    dauer = 120
    l, t = af_blocks(fname, dauer=dauer)
    plot_af(l, t)
    plot_blocks(fname)
    plt.show()
