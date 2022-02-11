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


baseline_correction = True
phasen = load_runs()
phasen = phasen[phasen.columns[:-2]].reset_index()

df = load_puls_alles()
df.drop(columns=["age", "sex", "group"], inplace=True)
phasen_cols = df.T[("", "phase")].copy()
puls = df[2:].sort_index()
if baseline_correction:
    pmean = puls.mean(axis=1)
    for c in puls.columns:
        puls[c] -= pmean


def select_cols(mask):
    mask = phasen[mask].nr.tolist()
    return phasen_cols.isin(mask)


def select(mask, run, puls=puls):
    mask = mask & (phasen.run == run)
    return puls.T[select_cols(mask)][run].melt(value_name="puls")


def compare_data(compare, column, runs=[1, 2], puls=puls):
    data = [
        pd.concat(
            [select(column == t, run=r, puls=puls) for t in compare],
            keys=compare,
            names=["trial"],
        )
        for r in runs
    ]
    return pd.concat(data, keys=runs, names=["run"]).reset_index()


def compare_plot(compare, column, runs=[1, 2]):
    data = compare_data(compare, column, runs=runs)
    fig = sns.violinplot(
        y="puls", x="run", data=data, hue="trial", split=True, inner="quart", bw=0.2
    )
    plt.xlabel("Run")
    return fig


if __name__ == "__main__":
    # Experiment 1: relax/stress Vergleich in den Phasen
    compare_plot(["relax", "stress"], phasen.trial_type, runs=[1, 2])
    plt.ylabel("Puls [bpm] baseline" if baseline_correction else "Puls [bpm]")
    plt.savefig(
        "stress_vs_relax_base.pdf" if baseline_correction else "stress_vs_relax_abs.pdf"
    )
    plt.show()
