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


def plot_af(l, t, dauer=60):
    plt.plot(t, l, label="Atemfreq")
    plt.xlabel('Zeit(s)')
    plt.ylabel('Atemfreq [1/%dsec]' % dauer)
    plt.title("peaks in resp curve")


def plot_blocks(fname):
    df = load_blocks()
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    plt.gca().axvspan(s0, t0, alpha = 0.2, color='red')
    plt.gca().axvspan(s1, t1, alpha = 0.2, color='blue')
    plt.gca().axvspan(s2, t2, alpha = 0.2, color='red')
    plt.legend()


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('file', nargs='*', default=["../../Daten/BekJan/HOAF_16.vhdr"],
                   help='Dateinamen, die angezeigt werden sollen')
    p.add_argument('-d', '--dauer', type=float,
                   help='Frequenzdauer')
    args = p.parse_args()
    for fname in args.file:
        l, t = af_blocks(fname, dauer=args.dauer)
        plt.figure(path.basename(fname))
        plot_af(l, t, dauer=args.dauer)
        plot_blocks(fname)
    plt.show()
