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


def select_cols(mask, pre_condition, run, puls, phasen):
    phasen_mask = pre_condition & mask & (phasen.run == run)
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
                        (criteria == t),
                        pre_condition=pre_condition,
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
    pre_condition=True,
    select=select_cols,
    bw=0.2,
    ylim=(-20, 30),
    file_name=None,
):
    global phasen, baseline_correction
    data = compare_data(
        compare, column, runs=runs, pre_condition=pre_condition, select=select
    )
    if file_name is not None:
        data[["run", "trial", "puls"]].to_csv(
            file_name, sep="\t", index=False, float_format="%05.2f"
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
        ["relax", "stress"],
        phasen.trial_type,
        runs=[1, 2],
        pre_condition=pre_condition,
        file_name="stress_vs_relax.tsv",
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


def select_rows(mask, pre_condition, run, puls, phasen):
    """Wie `select_cols`, nur dass Zeilen ausgewaelt werden.

    `pre_condition` wählt Spalten aus.
    """
    phasen_mask = pre_condition & (phasen.run == run)
    col_mask = phasen_cols.isin(phasen[phasen_mask].nr.tolist())
    return puls.loc[(run, mask), col_mask]


def musik_vs_sound():
    compare_plot(
        ["Musik", "Sound"],
        prob_info.group,
        runs=[1, 2],
        select=select_rows,
    )
    plt.title("Gesamte Zeit inklusive Pausen")
    savefig("musik_vs_sound_all")

    plt.figure()
    compare_plot(
        ["Musik", "Sound"],
        prob_info.group,
        runs=[1, 2],
        select=select_rows,
        pre_condition=(phasen.run > 0),
    )
    plt.title("Gesamte Zeit ohne Pausen")
    savefig("musik_vs_sound_both")

    plt.figure()
    compare_plot(
        ["Musik", "Sound"],
        prob_info.group,
        runs=[1, 2],
        select=select_rows,
        pre_condition=(phasen.trial_type == "stress"),
        file_name="musik_vs_sound_under_stress.tsv",
    )
    plt.title("Stress")
    savefig("musik_vs_sound_stress")

    plt.figure()
    compare_plot(
        ["Musik", "Sound"],
        prob_info.group,
        runs=[1, 2],
        select=select_rows,
        pre_condition=(phasen.trial_type == "relax"),
        file_name="musik_vs_sound_under_relex.tsv",
    )
    plt.title("Relax")
    savefig("musik_vs_sound_relax")


def statistics_example():
    data = compare_data(
        ["Musik", "Sound"],
        prob_info.group,
        runs=[1, 2],
        select=select_rows,
        pre_condition=(phasen.trial_type == "relax"),
    )
    data[["run", "trial", "puls"]].to_csv(
        "musik_vs_sound_under_relex.tsv", sep="\t", index=False, float_format="%05.2f"
    )


if __name__ == "__main__":
    baseline_correction = True
    load_data("puls_alles.tsv", baseline_correction=baseline_correction)
    print("geladen")

    # stress_vs_relax()
    # plt.figure()
    # math_vs_rotation(bw=0.1)
    # plt.figure()
    # wiederholung_12("stress")
    # wiederholung_12("relax")
    # stress_vs_relax_unterplots()

    musik_vs_sound()
    plt.show()
