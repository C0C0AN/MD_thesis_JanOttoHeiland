"""
Zählen der Peaks in Blöcken von zum Beispiel Minuten (60sec)
"""
from mne_atmung import number_peak
from matplotlib import pyplot as plt
from mne.preprocessing.peak_finder import peak_finder

fname = "../../Daten/BekJan/HOAF_16.vhdr"
data, times, raw = load_vhdr(fname)
datavector = data.reshape(-1)
threshold = (max(datavector)-min(datavector)) / 30

peak_loc, peak_mag = peak_finder(datavector,thresh=threshold, extrema=-1)
peak_times = times[peak_loc]



#def _peak_detection():
#    start = 0
#    stop = 10000
#
def number_peaks(start, stop):
    return len(peak_times[(peak_times >= start) & (peak_times < stop)])
#
#    pt_1 = peak_times[(peak_times>=start )& (peak_times<=stop)]
#
#    len(pt_1)

endzeit = times[-1]

start = 0
stop = 60
l = []
t = []
while stop <= endzeit:
    t.append(0.5*(start + stop))
    l.append(number_peaks(start, stop))
    start = start + 60
    stop = stop + 60


plt.plot(x,label="stress_1")
plt.xlabel('Zeit(s)')
plt.ylabel('Atmung')

plt.title("peaks in resp curve")

plt.legend()
plt.legend()
plt.gca().axvspan(1261.3976,1984.9446 facecolor='0.8',alpha = 0.5)
plt.gca().axvspan(3077.9946,3801.5416, facecolor='0.8',alpha = 0.5)

plt.show()