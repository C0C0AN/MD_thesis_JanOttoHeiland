
# coding: utf-8

import pandas as pd
import numpy as np
from scipy import *
import pingouin as pg
import matplotlib.pyplot as plt

#HOAF test sub 03 hier die 3 cortisolmessung verworfen, wenn nicht muss man noch mal bei den Zahlen unten verbessern
#2 Annahme 1 Mann = musik
#Habe alle Probanden mit eingeschlossen

df = pd.read_excel('../../Daten/Cortisol_werte/Cortisol_mit_baseline.xlsx', index_col=0)
c_diff = df.iloc[:,[0,4]]
c_diff_t = np.transpose(c_diff, axes=None)

#variabel für die Musikgruppe
music_a = [1,7,13,26,32,62,80,92,110,134,140,152,158,164,170]
music_b = [i+1 for i in music_a]
music_c = [i+1 for i in music_b]
music_d = [i+1 for i in music_c]
music_e = [i+1 for i in music_d]
music_f = [i+1 for i in music_e]

# da bei HOAF test sub 03 eine Messung zu viel war wurde die dritte Messung ausgelassen
music_e[2] = music_e[2] + 1
music_f[2] = music_f[2] + 1

#Variabel für die sound Gruppe
sound_a = [38,44,50,56,68,74,86,98,104,116,122,128,146]
sound_b = [i+1 for i in sound_a]
sound_c = [i+1 for i in sound_b]
sound_d = [i+1 for i in sound_c]
sound_e = [i+1 for i in sound_d]
sound_f = [i+1 for i in sound_e]

#variabel für die gesamte Gruppe
alle_a = music_a + sound_a
alle_b = music_b + sound_b
alle_c = music_c + sound_c
alle_d = music_d + sound_d 
alle_e = music_e + sound_e
alle_f = music_f + sound_f

#Zugriff Daten für die Musikgruppe
am = c_diff_t.iloc[:,music_a]
bm = c_diff_t.iloc[:,music_b]
cm = c_diff_t.iloc[:,music_c]
dm = c_diff_t.iloc[:,music_d]
em = c_diff_t.iloc[:,music_e]
fm = c_diff_t.iloc[:,music_f]

#Zugriff Daten für die soundgruppe
aw = c_diff_t.iloc[:,sound_a]
bw = c_diff_t.iloc[:,sound_b]
cw = c_diff_t.iloc[:,sound_c]
dw = c_diff_t.iloc[:,sound_d]
ew = c_diff_t.iloc[:,sound_e]
fw = c_diff_t.iloc[:,sound_f]

#Zugriff Daten für Varianz alle
av = c_diff_t.iloc[1,alle_a]
bv = c_diff_t.iloc[1,alle_b]
cv = c_diff_t.iloc[1,alle_c]
dv = c_diff_t.iloc[1,alle_d]
ev = c_diff_t.iloc[1,alle_e]
fv = c_diff_t.iloc[1,alle_f]

#Zugriff Daten Varianz music
amv = c_diff_t.iloc[1,music_a]
bmv = c_diff_t.iloc[1,music_b]
cmv = c_diff_t.iloc[1,music_c]
dmv = c_diff_t.iloc[1,music_d]
emv = c_diff_t.iloc[1,music_e]
fmv = c_diff_t.iloc[1,music_f]

#Zugriff Daten Varianz sound
awv = c_diff_t.iloc[1,sound_a]
bwv = c_diff_t.iloc[1,sound_b]
cwv = c_diff_t.iloc[1,sound_c]
dwv = c_diff_t.iloc[1,sound_d]
ewv = c_diff_t.iloc[1,sound_e]
fwv = c_diff_t.iloc[1,sound_f]



mean = a.iloc[1,:].mean(),b.iloc[1,:].mean(),c.iloc[1,:].mean(),d.iloc[1,:].mean(),e.iloc[1,:].mean(),f.iloc[1,:].mean()
np.asarray(mean)

mean_m = am.iloc[1,:].mean(),bm.iloc[1,:].mean(),cm.iloc[1,:].mean(),dm.iloc[1,:].mean(),em.iloc[1,:].mean(),fm.iloc[1,:].mean()
np.asarray(mean_m)

mean_w = aw.iloc[1,:].mean(),bw.iloc[1,:].mean(),cw.iloc[1,:].mean(),dw.iloc[1,:].mean(),ew.iloc[1,:].mean(),fw.iloc[1,:].mean()
np.asarray(mean_w)

vara_alle = av.var(axis=None),bv.var(axis=None),cv.var(axis=None),dv.var(axis=None),ev.var(axis=None),fv.var(axis=None)
vara_musik = amv.var(axis=None),bmv.var(axis=None),cmv.var(axis=None),dmv.var(axis=None),emv.var(axis=None),fmv.var(axis=None)
vara_sound = awv.var(axis=None),bwv.var(axis=None),cwv.var(axis=None),dwv.var(axis=None),ewv.var(axis=None),fwv.var(axis=None)

stda_alle = av.std(axis=None),bv.std(axis=None),cv.std(axis=None),dv.std(axis=None),ev.std(axis=None),fv.std(axis=None)
stda_music = amv.std(axis=None),bmv.std(axis=None),cmv.std(axis=None),dmv.std(axis=None),emv.std(axis=None),fmv.std(axis=None)
stda_sound = awv.std(axis=None),bwv.std(axis=None),cwv.std(axis=None),dwv.std(axis=None),ewv.std(axis=None),fwv.std(axis=None)

vara_alle
vara_musik
vara_sound

stda_alle
stda_music
stda_sound

#plot einer Gruppe
get_ipython().magic(u'matplotlib inline')
plt.plot(mean_w)
plt.xlabel('Zeitpunkte')
plt.ylabel('Cortisol nmol/L')
plt.title("Mittelwerte der Cortisolmessungen in der Sound Gruppe")

#plot zwei Gruppen gegeneinander
get_ipython().magic(u'matplotlib inline')
fig, ax = plt.subplots()
ax.plot(mean_m, label='musik')
ax.plot(mean_w, label='sound')
plt.xlabel('Zeitpunkte')
plt.ylabel('Cortisol nmol/L')
plt.title("Mittelwerte Cortisol beide Gruppen")
plt.legend()