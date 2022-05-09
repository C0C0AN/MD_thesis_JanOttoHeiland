import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ezodf

from data import DATEN_DIR

VERZEICHNIS = f"{DATEN_DIR}/physio_resp_pulse/physio_sub_version"
file_ma = f"{VERZEICHNIS}/sub_combined.ods"

# Importiere Daten
dm = pd.read_csv(
    f"{VERZEICHNIS}/Musik_run1_2.csv",
    header=0,
    usecols=[0],
)
dm.loc[:, ("Musik_r1_2\t")].astype(float)
dm = dm.dropna()
dw = pd.read_csv(
    f"{VERZEICHNIS}/sound_run1_2.csv",
    header=0,
    usecols=[0],
)
dw.loc[:, ("sound_run1_2")].astype(float)
dw = dw.dropna()
dwm = pd.read_csv(
    f"{VERZEICHNIS}/musik_sound_r1_2.csv",
    header=0,
    usecols=[0],
)
dwm.loc[:, ("musik_sound_r1_2")].astype(float)
dwm = dwm.dropna()
dmr1 = pd.read_csv(
    f"{VERZEICHNIS}/m_r1_mean.csv",
    header=0,
    usecols=[0],
)
dmr1.loc[:, ("m_r1_mean")].astype(float)
dmr1 = dmr1.dropna()
dwr1 = pd.read_csv(
    f"{VERZEICHNIS}/s_r1_mean.csv",
    header=0,
    usecols=[0],
)
dwr1.loc[:, ("s_r1_mean")].astype(float)
dwr1 = dwr1.dropna()
dmr2 = pd.read_csv(
    f"{VERZEICHNIS}/m_r2_mean.csv",
    header=0,
    usecols=[0],
)
dmr2.loc[:, ("m_r2_mean")].astype(float)
dmr2 = dmr2.dropna()
dwr2 = pd.read_csv(
    f"{VERZEICHNIS}/sr2_mean.csv",
    header=0,
    usecols=[0],
)
dwr2.loc[:, ("sr2_mean")].astype(float)
dwr2 = dwr2.dropna()
time = pd.read_csv(
    f"{VERZEICHNIS}/time.csv",
    header=0,
    usecols=[0],
)
time.loc[:, ("time")].astype(float)

mean_m = dm.mean(axis=None, level=None, numeric_only=None)
std_m = dm.std(axis=None, level=None, ddof=1, numeric_only=None)
mean_w = dw.mean(axis=None, level=None, numeric_only=None)
std_w = dw.std(axis=None, level=None, ddof=1, numeric_only=None)
mean_mw = dwm.mean(axis=None, level=None, numeric_only=None)
std_mw = dwm.std(axis=None, level=None, ddof=1, numeric_only=None)

log_dwm = np.log(dwm["musik_sound_r1_2"])
sqrt_dwm = np.sqrt(dwm["musik_sound_r1_2"])

# Erzeugen eines DataFrames
doc_ma = ezodf.opendoc(file_ma)

print("Spreadsheet contains %d sheet(s)." % len(doc_ma.sheets))
for sheet in doc_ma.sheets:
    print("-" * 40)
    print("   Sheet name : '%s'" % sheet.name)
    print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()))

# convert the first sheet to a pandas.DataFrame
sheet_ma = doc_ma.sheets[0]
df_dict_ma = {}
for i, row in enumerate(sheet_ma.rows()):
    # row is a list of cells
    # assume the header is on the first row
    if i == 0:
        # columns as lists in a dictionary
        df_dict_ma = {cell.value: [] for cell in row}
        # create index for the column headers
        col_index_ma = {j: cell.value for j, cell in enumerate(row)}
        continue
    for j, cell in enumerate(row):
        # use header instead of column index
        df_dict_ma[col_index_ma[j]].append(cell.value)
# and convert to a DataFrame
df_ma = pd.DataFrame(df_dict_ma)

# extrahieren der Daten für die einzelnen Stressphasen und bilden eines Mittelwertes
prob = [c for c in df_ma.columns if c.startswith("p")]
prob1 = [p for p in prob if p.endswith(":1")]
prob2 = [p for p in prob if p.endswith(":2")]
# Maximaler Mittelwert Unterschied Exel vs. python
pandas_diff_excel = df_ma[prob2].mean(axis=1) - df_ma.Mittelwert_2
pandas_diff_excel.abs().max()

# baseline und z-score Korrektur
df_mb = df_ma[prob1 + prob2].copy()
df_mb = df_mb - df_mb.mean(axis=0)
df_mc = (df_mb - df_mb.mean(axis=0)) / df_mb.std(
    axis=0
)  # z-score: normalize with respect to standard deviation
df_mb

# Plots der Rohdaten
# Methode um Pulsdaten in den zwei Stressblöcken zu plotten
def plot_puls(prob1, label, df=df_ma, color="orange", ax=None, lw1=1):
    ax1 = df[prob1].plot(legend=None, color=color, alpha=0.2, linewidth=lw1, ax=ax)
    df[prob1].mean(axis=1).plot(label=label, linewidth=2, color=color, ax=ax1)
    return ax1


fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
plot_puls(prob1, "Stress1", ax=ax1)
plot_puls(prob2, "Stress2", color="blue", ax=ax2)
ax2.legend(["Stress2"])
ax1.legend(["Stress1"], loc="upper right")
plt.xlabel("Zeit [sec]/TR [1.45 sec]")
ax1.set_title(" Pulsdaten")
fig.text(0.045, 0.5, "Puls (bpm)", ha="center", va="center", rotation="vertical")
plt.savefig("puls_XXX.pdf")

# plot der Stressphasen für die Gruppen Musik und Sound
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle("Aligning x-axis using sharex")

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax2.plot(dmr2, label="musik", color="#ed77dd")
ax2.plot(dwr2, label="sound", color="#e82354")
ax1.plot(dmr1, label="musik", color="#ed77dd")
ax1.plot(dwr1, label="sound", color="#e82354")
plt.legend()
ax1.set_title("Stressblock1")
ax2.set_title("Stressblock2")
ax1.set_label("Stressblock1")
ax2.set_label("Stressblock2")

fig.text(0.5, 0.04, "Zeit[sec]/TR[1,45 sec]", ha="center", va="center")
fig.text(0.06, 0.5, "Puls (bpm)", ha="center", va="center", rotation="vertical")
plt.savefig("stressblock1")

# Definiere Phasen der Stressblöcke
phases = [
    (4, 106.206896552),
    (125.517241379, 227.586206897),
    (246.896551724, 348.965517241),
    (368.275862069, 470.344827586),
]

# Methode zum Zugriff auf die Stress und Entspannungsphasen des Experiments
def plot_phases(colors=["0.3", "0.9"], alpha=0.06):
    for i, phase in enumerate(phases):
        plt.axvspan(phase[0], phase[1], facecolor=colors[i % 2], alpha=alpha)


# Pulsdaten der Stressblöcke 1 und 2, dargestellt in den verschiedenen Stress und Entspannungsphasen.
plot_phases(colors=["violet", "green"], alpha=0.03)
ax1 = plot_puls(prob1, "Stress1", color="blue", ax=plt.gca(), df=df_mb, lw1=0.5)
plot_puls(prob2, "Stress2", color="orange", ax=ax1, df=df_mb, lw1=0.5)
plt.xlabel("Zeit [sec]/ TR [1.45 sec]")
plt.text(15, -17.5, "Phase", fontsize=10)
plt.text(67, -17.5, "a/", fontsize=10, color="blue")
plt.text(82, -17.5, "a`", fontsize=10, color="orange")
plt.text(140, -17.5, "Phase ", fontsize=10)
plt.text(190, -17.5, "b/", fontsize=10, color="blue")
plt.text(207, -17.5, "b`", fontsize=10, color="orange")
plt.text(260, -17.5, "Phase ", fontsize=10)
plt.text(312, -17.5, "c/", fontsize=10, color="blue")
plt.text(327, -17.5, "c`", fontsize=10, color="orange")
plt.text(380, -17.5, "Phase ", fontsize=10)
plt.text(430, -17.5, "d/", fontsize=10, color="blue")
plt.text(446, -17.5, "d`", fontsize=10, color="orange")
plt.ylabel("Puls(bpm) to baseline")
plt.title("Pulsdaten baseline korrigiert")
plt.savefig("puls_mb.pdf")

# Pulsdaten der Stressblöcke 1 und 2, dargestellt in den verschiedenen Stress und Entspannungsphasen.
# baseline und z-score korrigiert
plot_phases(colors=["violet", "green"], alpha=0.03)
ax1 = plot_puls(prob1, "Stress1", color="blue", ax=plt.gca(), df=df_mc, lw1=0.5)
plot_puls(prob2, "Stress2", color="orange", ax=ax1, df=df_mc, lw1=0.5)

plt.xlabel("Zeit [sec]/ TR [1.45 sec]")
plt.text(15, -2.9, "Phase", fontsize=10)
plt.text(67, -2.9, "a/", fontsize=10, color="blue")
plt.text(82, -2.9, "a`", fontsize=10, color="orange")
plt.text(140, -2.9, "Phase ", fontsize=10)
plt.text(190, -2.9, "b/", fontsize=10, color="blue")
plt.text(207, -2.9, "b`", fontsize=10, color="orange")
plt.text(260, -2.9, "Phase ", fontsize=10)
plt.text(312, -2.9, "c/", fontsize=10, color="blue")
plt.text(327, -2.9, "c`", fontsize=10, color="orange")
plt.text(380, -2.9, "Phase ", fontsize=10)
plt.text(430, -2.9, "d/", fontsize=10, color="blue")
plt.text(446, -2.9, "d`", fontsize=10, color="orange")
plt.ylabel("Puls(bpm) to baseline")
plt.title("Puls [z-score]")
plt.savefig("puls_mc.pdf")

# Zugriff auf Mittelwerte der Stressphase 1 (phase_mean1)
phase_mean1 = [
    df_mb.loc[range(int(p[0]), int(p[1]))][prob1].mean(axis=0).mean() for p in phases
]

# Zugriff auf Mittelwerte der Stressphase 2 (phase_mean2)
phase_mean2 = [
    df_mb.loc[range(int(p[0]), int(p[1]))][prob2].mean(axis=0).mean() for p in phases
]


def plot_mean_phases(phase_mean1=phase_mean1, color="orange"):
    """Methode zum Plotten der Mittelwerte der Stress und Entspannungsphasen"""
    for i, mid in enumerate(phase_mean1):
        plt.hlines(y=mid, xmin=phases[i][0], xmax=phases[i][1], color=color)


# Plot der Mittelwerte in den Phasen
plot_phases(colors=["violet", "green"], alpha=0.03)
plt.xlabel("Zeit [sec]")
plot_mean_phases(phase_mean1, color="blue")
plot_mean_phases(phase_mean2, color="orange")
plt.savefig("puls_mean_phases.pdf")

# Mittelwerte der Phasen
mean_1 = (78.746, 83.038, 74.511, 76.613)
mean_2 = (79.679, 77.405, 79.594, 73.424)
stda_1 = (2.786, 2.948, 2.677, 2.673)
stda_2 = (3.171, 2.919, 3.154, 2.600)

# plot der Mittelwerte und Standartfehler über die Phasen des Experiments hinweg
x_achse = [
    53,
    180,
    300,
    420,
]
x1_achse = [58, 185, 305, 425]
fig, ax = plt.subplots()
plot_phases(colors=["violet", "green"], alpha=0.03)
ax.errorbar(
    x_achse, mean_1, yerr=stda_1, fmt="-o", capsize=3, label="stress_1", color="blue"
)
ax.errorbar(
    x1_achse, mean_2, yerr=stda_2, fmt="-^", capsize=3, label="stress_2", color="orange"
)
plt.xlabel("Zeit(s)/TR(1,45s)")
plt.text(15, 70.5, "Phase", fontsize=10)
plt.text(67, 70.5, "a/", fontsize=10, color="blue")
plt.text(82, 70.5, "a`", fontsize=10, color="orange")
plt.text(140, 70.5, "Phase ", fontsize=10)
plt.text(190, 70.5, "b/", fontsize=10, color="blue")
plt.text(207, 70.5, "b`", fontsize=10, color="orange")
plt.text(260, 70.5, "Phase ", fontsize=10)
plt.text(312, 70.5, "c/", fontsize=10, color="blue")
plt.text(327, 70.5, "c`", fontsize=10, color="orange")
plt.text(380, 70.5, "Phase ", fontsize=10)
plt.text(430, 70.5, "d/", fontsize=10, color="blue")
plt.text(446, 70.5, "d`", fontsize=10, color="orange")
plt.ylabel("Puls (bpm)")
ax.set_title("Mittelwert und Standartfehler")
plt.legend()
plt.savefig("mean_puls.png")
