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


def load_data(file_name="puls_alles.tsv", baseline_correction=True):
    global phasen, puls, phasen_cols
    phasen = load_runs()
    phasen = phasen[phasen.columns[:-2]].reset_index()
    df = load_puls_alles()
    phasen_cols = df.T[("", "phase")].dropna()
    puls = df.drop(columns=["age", "sex", "group"])[2:].sort_index()
    if baseline_correction:
        pmean = puls.mean(axis=1)
        for c in puls.columns:
            puls[c] -= pmean


def select_cols(mask):
    mask = phasen[mask].nr.tolist()
    return phasen_cols.isin(mask)


def select(mask, run):
    global puls, phasen
    cols = mask & (phasen.run == run)
    return puls.T[select_cols(cols)][run]


def compare_data(
        compare, column, runs=[1, 2], pre_condition=None,
):
    global phasen
    if pre_condition is None:
        pre_condition = (phasen.run > 0)
    return pd.concat(
        [
            pd.concat(
                [
                    select(pre_condition & (column == t), run=r).melt(
                        value_name="puls"
                    )
                    for t in compare
                ],
                keys=compare,
                names=["trial"],
            )
            for r in runs
        ],
        keys=runs,
        names=["run"],
    ).reset_index()


def compare_plot(compare, column, runs=[1, 2], bw=0.2, pre_condition=None, ylim=(-20, 30)):
    global phasen, baseline_correction
    if pre_condition is None:
        pre_condition = (phasen.run > 0)
    data = compare_data(compare, column, runs=runs, pre_condition=pre_condition)
    fig = sns.violinplot(
        y="puls", x="run", data=data, hue="trial", split=True, inner="quart", bw=bw
    )
    plt.ylabel("Puls [bpm] baseline" if baseline_correction else "Puls [bpm]")
    plt.xlabel("Run")
    plt.ylim(ylim)
    return fig


def stress_vs_relax(pre=None):
    """Experiment 1: relax/stress Vergleich in den Phasen"""
    compare_plot(["relax", "stress"], phasen.trial_type, runs=[1, 2], pre_condition=pre)
    plt.savefig(
        "stress_vs_relax_base.pdf" if baseline_correction else "stress_vs_relax_abs.pdf"
    )
    plt.legend().set_title("Stimulus")


def math_vs_rotation(bw=0.2):
    """Experiment 2: Vergleiche math vs rotation."""
    compare_plot(["math", "rotation"], phasen.condition, runs=[1, 2], bw=bw)
    plt.savefig(
        "math_vs_rotation_" + ("base" if baseline_correction else "abs") + ".pdf"
    )
    plt.legend().set_title("Aufgabentyp")


def wiederholung_12(trial_type="stress"):
    compare_plot(
        [1, 2],
        phasen.repetition,
        runs=[1, 2],
        pre_condition=(phasen.trial_type == trial_type),
    )
    plt.legend().set_title("Wiederholung")
    plt.title(trial_type.capitalize())
    plt.savefig(
        f"{trial_type}_wiederholung_"
        + ("base" if baseline_correction else "abs")
        + ".pdf"
    )

if __name__ == "__main__":
    # stress_vs_relax()
    # plt.figure()
    # math_vs_rotation(bw=0.1)
    # wiederholung_12("stress")
    # wiederholung_12("relax")
    baseline_correction = True
    load_data("puls_alles.tsv", baseline_correction=baseline_correction)

    stress_vs_relax()
    plt.figure()
    stress_vs_relax(pre=(phasen.condition == "math"))
    plt.title("Aufgabe: Mathematik")
    plt.figure()
    stress_vs_relax(pre=(phasen.condition == "rotation"))
    plt.title("Aufgabe: Rotation")
    plt.show()
