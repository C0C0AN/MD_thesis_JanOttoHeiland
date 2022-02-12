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
    global phasen, puls, phasen_cols, prob_info
    phasen = load_runs()
    phasen = phasen[phasen.columns[:-2]].reset_index()
    df = load_puls_alles()
    phasen_cols = df.T[("", "phase")].dropna()
    prob_info = df[["age", "sex", "group"]].copy().dropna().sort_index()
    puls = df.drop(columns=["age", "sex", "group"])[2:].sort_index()
    if baseline_correction:
        pmean = puls.mean(axis=1)
        for c in puls.columns:
            puls[c] -= pmean


def select_cols(mask, run, puls, phasen):
    phasen_mask = mask & (phasen.run == run)
    col_mask = phasen_cols.isin(phasen[phasen_mask].nr.tolist())
    return puls.loc[(run, slice(None)), col_mask]


def compare_data(
    compare,
    criteria,
    runs=[1, 2],
    pre_condition=True,
    select=select_cols,
):
    global phasen, puls

    return pd.concat(
        [
            pd.concat(
                [
                    select(
                        pre_condition & (criteria == t),
                        run=r,
                        puls=puls,
                        phasen=phasen,
                    ).melt(value_name="puls")
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


def compare_plot(
    compare,
    column,
    runs=[1, 2],
    bw=0.2,
    ylim=(-20, 30),
    pre_condition=True,
    select=select_cols,
):
    global phasen, baseline_correction
    data = compare_data(
        compare, column, runs=runs, pre_condition=pre_condition, select=select
    )
    fig = sns.violinplot(
        y="puls", x="run", data=data, hue="trial", split=True, inner="quart", bw=bw
    )
    plt.ylabel("Puls [bpm] baseline" if baseline_correction else "Puls [bpm]")
    plt.xlabel("Run")
    plt.ylim(ylim)
    return fig


def stress_vs_relax(pre_condition=None):
    """Experiment 1: relax/stress Vergleich in den Phasen"""
    compare_plot(
        ["relax", "stress"], phasen.trial_type, runs=[1, 2], pre_condition=pre_condition
    )
    plt.savefig(
        "stress_vs_relax_" + ("base" if baseline_correction else "abs") + ".pdf"
    )
    plt.legend().set_title("Stimulus")


def savefig(file_name):
    global baseline_correction
    plt.savefig(file_name + ("base" if baseline_correction else "abs") + ".pdf")


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


def stress_vs_relax_unterplots():
    stress_vs_relax()
    plt.figure()
    stress_vs_relax(pre_condition=(phasen.condition == "math"))
    plt.title("Aufgabe: Mathematik")
    plt.figure()
    stress_vs_relax(pre_condition=(phasen.condition == "rotation"))
    plt.title("Aufgabe: Rotation")


def musik_vs_sound():
    def select_rows(mask, run, puls, phasen):
        return puls.loc[(run, mask), :]

    def select_stress_rows(mask, run, puls, phasen):
        phasen_mask = (phasen.trial_type == "stress") & (phasen.run == run)
        stress_cols = phasen_cols.isin(phasen[phasen_mask].nr.tolist())
        return puls.loc[(run, mask), stress_cols]

    compare_plot(
        ["Musik", "Sound"],
        prob_info.group,
        runs=[1, 2],
        select=select_rows,
    )
    plt.title("Stress und Relax")
    savefig("musik_vs_sound_all")
    plt.figure()

    compare_plot(
        ["Musik", "Sound"],
        prob_info.group,
        runs=[1, 2],
        select=select_stress_rows,
    )
    plt.title("Stress")
    savefig("musik_vs_sound_stress")


if __name__ == "__main__":
    baseline_correction = True
    load_data("puls_alles.tsv", baseline_correction=baseline_correction)
    print("geladen")

    # stress_vs_relax()
    # plt.figure()
    # math_vs_rotation(bw=0.1)
    # wiederholung_12("stress")
    # wiederholung_12("relax")
    # stress_vs_relax_unterplots()

    musik_vs_sound()
    plt.show()
