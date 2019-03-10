# coding: utf-8
from __future__ import print_function
import mne
import os.path as op
import numpy as np
from matplotlib import pyplot as plt
from mne.io import read_raw_brainvision

from numpy.testing import assert_array_equal
import os
import numpy as np
from mne.preprocessing.peak_finder import peak_finder

plot_resp = False


def load_vhdr(file='/home/jan/Documents/Doktorarbeit/Daten/BekJan/HOAF_EDA_Resp0002.vhdr'):

    raw = mne.io.read_raw_brainvision(file, preload=True)
    data = raw.get_data()
    # fig = raw.plot(None, 10.0,0.0,3,'w',None,(0.8,0.8,0.8),'cyan','auto')
    raw.pick_channels(['Resp'])
    data, times = raw[:]
    # TODO: 20218200 = ??
    return data, times, raw

if plot_resp:
    plt.vlines(x=peak_times, ymin=-1, ymax=1)
    plt.plot(times, resp)


def plot_test_range(a=3000, b=3300):
    """
    Plot the respiration data in the range from a to b (seconds)
    """
    a = np.where(times >= a)[0][0]
    b = np.where(times <= b)[0][-1]
    a = 0; b = len(times)
    tresp = resp[a:b]
    thres = default
    tpeak_loc, _ = peak_finder(tresp, thresh=thres, extrema=-1)
    tpeak_times = times[a:b][tpeak_loc]
    if False:
        plt.vlines(x=tpeak_times, ymin=-1, ymax=1)
        plt.plot(times[a:b], tresp)

    plt.xlabel(u"Intervalllänge")
    plt.hist(np.diff(tpeak_times), bins=np.linspace(0, 7.5, num=100), 
              label="Verteilung der Atmungsintervalllaengen", density=True)


if __name__ == '__main__':
    import sys

    file = '/home/jan/Documents/Doktorarbeit/Daten/BekJan/HOAF_EDA_Resp0002.vhdr'
    if len(sys.argv) >= 2:
        file = sys.argv[1]
    print("Loading", file)
    data, times, raw = load_vhdr(file)
    datavector=np.reshape(data, 20218200)
    default = (max(datavector)-min(datavector))/30

    #Einspeisen des Datenvektors in peakfinder 
    peak_loc, peak_mag = peak_finder(datavector,thresh=default, extrema=-1)
    peak_times = times[peak_loc]
    resp = raw.get_data()[0]

    plot_test_range()
    plt.show()


def rest():
    start = 1098
    stop = 1822


    # In[26]:


    def number_peak(start =start, stop=stop):
        return len(peak_times[(peak_times>=start )& (peak_times<=stop)])




    # In[27]:


    pt_1 = peak_times[(peak_times>=start )& (peak_times<=stop)]


    # In[28]:


    len(pt_1)


    # In[29]:


    times[20120541]


    # In[30]:


    # min(datavector)


    # # In[31]:


    # max(datavector)


    # # In[32]:


    # number_peak()


    # # In[49]:


    # #time rc1 start
    # rc1a = times[5365177]+6


    # # In[50]:


    # #time rc1 stop
    # 1rc1e = times[5365177]+66


    # # In[51]:


    # #time mc1 start
    # 1mc1a = times[5365177]+94


    # # In[52]:


    # #time mc1 stop
    # 1mc1e = times[5365177]+152


    # # In[53]:


    # #time rs1 start
    # 1rs1a = times[5365177]+182


    # # In[54]:


    # #time rs1 stop
    # 1rs1e = times[5365177]+242


    # # In[55]:


    # #time ms1 start
    # 1ms1a = times[5365177]+270


    # # In[57]:


    # #time ms1 stop
    # 1ms1e = times[5365177]+330


    # # In[ ]:


    # #time rc2 start
    # 1rc2a = times[5365177]+358


    # # In[58]:


    # #time rc2 stop
    # 1rc2e = times[5365177]+413


    # # In[59]:


    # #time mc2 start
    # 1mc2a = times[5365177]+446


    # # In[60]:


    # #time mc2 stop
    # 1mc2e = times[5365177]+501


    # In[61]:


    #time rs2 start
    # 1rs2a = times[5365177]+534


    # In[62]:


    # #time rs2 stop
    # 1rs2e = times[5365177]+594


    # # In[63]:


    # #time ms2 start
    # 1ms2a = times[5365177]+622


    # # In[67]:


    # #time ms2 stop
    # 1ms2e = times[5365177]+682


    # # In[65]:


    # #Zeitspanne erster Stressblock
    # times[8982913]-times[5365177]


    # # In[40]:


    # #Zeitspanne zweiter Stressblock
    # times[17888542]-times[14270812]

