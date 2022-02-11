"""Plotte vergleichend Pulsdaten."""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from puls_collect import load_runs


def load_puls_alles(file_name="puls_alles.tsv"):
    df = pd.read_csv(file_name, sep="\t", index_col=[0, 1])
    df = df.set_index(
        pd.MultiIndex.from_tuples(
            [
                ("" if np.isnan(a) else int(a), int(b) if b.isdecimal() else b)
                for a, b in df.index
            ],
            names=df.index.names,
        )
    )
    return df


runs = load_runs()
runs = runs[runs.columns[:-2]].reset_index()

df = load_puls_alles()
df.drop(columns=["age", "sex", "group"], inplace=True)
phasen = df.T[("", "phase")].copy()

# Experiment 1: relax/stress Vergleich in den Runs
def select(mask, run, df=df):
    mask = runs[mask].nr.tolist()
    return df.T[phasen.isin(mask)][run].copy().melt(value_name="puls")


relax1 = select((runs.run == 1) & (runs.trial_type == "relax"), run=1)
stress1 = select((runs.run == 1) & (runs.trial_type == "stress"), run=1)
relax2 = select((runs.run == 2) & (runs.trial_type == "relax"), run=2)
stress2 = select((runs.run == 2) & (runs.trial_type == "stress"), run=2)

data1 = pd.concat((relax1, stress1), keys=["relax", "stress"], names=["trial type"])
data2 = pd.concat((relax2, stress2), keys=["relax", "stress"], names=["trial type"])
data = pd.concat((data1, data2), keys=[1, 2], names=["run"])

data = data.reset_index()
fig = sns.violinplot(
    y="puls", x="run", data=data, hue="trial type", split=True, inner="quart", bw=0.2
)
plt.ylabel("Puls [bpm]")
plt.xlabel("Run")
plt.savefig("stress_vs_relax.pdf")
plt.show()
