"""Plotte vergleichend Pulsdaten."""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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


df = load_puls_alles()
df.drop(columns=["age", "sex", "group"], inplace=True)

# Experiment 1: relax/stress Vergleich in den Runs
phasen = df.T[('', 'phase')]
relax1 = df.T[phasen.isin([1, 2, 5, 6])][1].melt()["value"]
stress1 = df.T[phasen.isin([3, 4, 7, 8])][1].melt()["value"]

data = pd.concat((relax1, stress1), keys=[0, 1], names=["sr"]).reset_index()[["sr", "value"]]
data["run"] = 1
sns.violinplot(y="value", x="run", data=data, hue="sr", split=True, inner="quart", bw=0.1)
plt.show()
