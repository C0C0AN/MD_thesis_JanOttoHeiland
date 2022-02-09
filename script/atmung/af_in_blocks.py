# coding: utf-8
"""
Zählen der Peaks in Blöcken von zum Beispiel Minuten (60sec)
"""
from resp import load_vhdr
from blocks import load_blocks
from matplotlib import pyplot as plt
from mne.preprocessing.peak_finder import peak_finder
from os import path
import numpy as np
from scipy import signal

def number_peaks(peak_times, start, stop):
    return len(peak_times[(peak_times >= start) & (peak_times < stop)])

#
#def af_blocks(fname, dauer=30, schritt=1.45, start=0, endzeit=None):
#    '''
#    return af /min Zeit(xAchse), peak loc: Peaks des eindimensionalen datavectors
#    times: Zeitpunkte der Peaks, peak_mag: Aulenkung der Peaks. 
#
#    '''
#    data, times, raw = load_vhdr(fname)
#    datavector = data.reshape(-1)
#    threshold = (max(datavector)-min(datavector)) / 15
#
#    peak_loc, peak_mag = peak_finder(datavector,thresh=threshold, extrema=-1)
#    peak_times = times[peak_loc]
#
#    if endzeit is None:
#        endzeit = times[-1]
#    stop = start + dauer
#    freq = []
#    point = []
#    while stop <= endzeit:
#	'''
#	Das Fenster in dem die Peaks gezählt werden verschiebt sich immer 
#	um eine gewisse Zeit (Schritt), Der Wert der ermittelten Peaks, wird 
#	immer in die Mitte eines solchen Intervalls geschrieben, sodass am 
#	Anfang und am Ende eine Zeitlücke simuliert wird. 	
#	'''
#          
#        point.append(0.5*(start + stop))
#        freq.append(number_peaks(peak_times, start, stop))
#        start = start + schritt
#        stop = stop + schritt
#        
##        point.append(start)
##        freq.append(number_peaks(peak_times, start-0.5*dauer, start+0.5*dauer))
##        start = start + schritt
##        stop = stop + schritt
#    return freq, point

def af_blocks(fname, dauer=30, schritt=1.45, start=0, endzeit=None):
    '''
    return af /min Zeit(xAchse), peak loc: Peaks des eindimensionalen datavectors
    times: Zeitpunkte der Peaks, peak_mag: Aulenkung der Peaks. 

    '''
    print(start)
    data, times, raw = load_vhdr(fname)
    datavector = data.reshape(-1)
    threshold=0.6*datavector.std()

    peak_loc, peak_mag = peak_finder(datavector,thresh=threshold, extrema=-1)
    peak_times = times[peak_loc]
	
    anzahlpeaks=peak_loc.size
    atemzugdauer_mittelwert=(times[-1]-times[0])/anzahlpeaks 

    if endzeit is None:
        endzeit = times[-1]
    #stop = start + dauer
    freq = []
    point = []
    while start <= endzeit:
        s=start - 0.5*dauer
        e=s+dauer
        indices=np.where((peak_times >= s) & (peak_times <= e))
        #display(indices)
        if (np.size(indices)>0):
            mini=np.min(indices) 
            if (mini > 0):
                dauer_erster_atemzug=peak_times[mini]-peak_times[mini-1]
            else:
        			dauer_erster_atemzug=atemzugdauer_mittelwert            
            fremdanteil_erster_atemzug=peak_times[mini]-s
    
            maxi=np.max(indices) 
            if (maxi< (peak_times.size -1)):
        			dauer_letzter_atemzug=peak_times[maxi]-peak_times[maxi+1]
            else:
        			dauer_letzter_atemzug=atemzugdauer_mittelwert
    
            fremdanteil_letzter_atemzug=e - peak_times[maxi]
            anzahl=number_peaks(peak_times, s, e) + (fremdanteil_erster_atemzug / dauer_erster_atemzug) + (fremdanteil_letzter_atemzug / dauer_letzter_atemzug)
            
            point.append(start)
            if (s<0):
                freq.append(anzahl/(e))    
            else:
                if (e>endzeit):
                    freq.append(anzahl/(endzeit-s))
                else:
                    freq.append(anzahl/dauer)
        else:
            point.append(start)
          #  freq.append(-1.0)
           # display("Murks am Ende")
        start = start + schritt
    return freq, point

def plot_af(l, t, dauer=60):
    plt.plot(t, l, label="Atemfreq")
    plt.xlabel('Zeit(s)')
    plt.ylabel('Atemfreq [1/%dsec]' % dauer)
    plt.title("peaks in resp curve")


def plot_blocks(fname):
    '''
    so-t2 sind die Anfangs und Endzeiten von allen 3 Blöcken in chronologischer Reihenfolge
    definiert über die REsponseantwort während der Blöcke. 
    '''
    df = load_blocks()
    s0, t0, s1, t1, s2, t2 = df.loc[path.basename(fname)]
    plt.gca().axvspan(s0, t0, alpha = 0.2, color='red')
    plt.gca().axvspan(s1, t1, alpha = 0.2, color='blue')
    plt.gca().axvspan(s2, t2, alpha = 0.2, color='red')
    plt.legend()


if __name__ == '__main__':
    import argparse
    '''
    dauer: Zeitfenster in dem die Peaks gezählt werden, 
    schritt: er Zeitabstand, um den sich dieses Fenster verschiebt
    '''

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('file', nargs='*', default=["../../Daten/BekJan/HOAF_16.vhdr"],
                   help='Dateinamen, die angezeigt werden sollen')
    p.add_argument('-d', '--dauer', type=float, default=60,
                   help='Frequenzdauer')
    p.add_argument('-s', '--step', type=float, default=5,
                   help='Moving average window size')
    args = p.parse_args()

    for fname in args.file:
        l, t = af_blocks(fname, dauer=args.dauer, schritt=args.step)
        plt.figure(path.basename(fname))
        plot_af(l, t, dauer=args.dauer)
        plot_blocks(fname)
    plt.show()
