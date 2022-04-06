# coding: utf-8
"""Suche alle Informationen ueber die Pulsdaten zusammen und schreibe sie nach `puls_alles.tsv`."""
import numpy as np
import pandas as pd
from phases_analyze import load_phasen
from data import DATEN_DIR


def load_runs():
    runs = load_phasen("../phasen.tsv")
    runs["nr"] = list(range(8)) + list(range(8))
    runs = runs.reset_index().set_index(["run", "nr"])
    return runs


def run_intervals(runs=None):
    runs = runs or load_runs()
    # mittlere Start- und End-Zeiten der Phasen
    run = runs.groupby("nr").mean()
    run.repetition = run.repetition.astype(int)
    return pd.IntervalIndex.from_arrays(run.start, run.end)


def load_group_info():
    """Lade Gruppezugehoerigkeit."""
    from data import HOAF_BIDS
    from os import path

    prob = pd.read_csv(path.join(HOAF_BIDS, "participants.tsv"), sep="\t")
    prob["prob_nr"] = prob.participant_id.str.extract(r"sub-(.+)").astype(int)
    prob = prob.set_index("prob_nr")
    prob = prob.dropna()
    prob = prob.drop(columns=["participant_id"])
    extra = pd.concat((prob, prob), keys=[1, 2])
    extra.index.set_names(["run", "prob_nr"])
    return extra


if __name__ == "__main__":
    file_ma = DATEN_DIR + "/physio_resp_pulse/physio_sub_version/sub_combined.ods"
    df = pd.read_excel(file_ma)
    # df = df.round(0).astype(int)
    df = df[[c for c in df.columns if not c.startswith("Mittelwert")]]
    df = df.T
    df["run"] = df.index.str.extract(r".+\:([12])").astype(int).values
    df["prob_nr"] = df.index.str.extract(r"[pP](.+):.*").astype(int).values
    df = df.reset_index(drop=True).set_index(["prob_nr", "run"])
    df = df.T
    df["time"] = [i * 1.45 for i in df.index]

    runs = load_runs()
    intervals = run_intervals(runs)
    phase = pd.cut(df.time, intervals, labels=False)
    df["phase"] = phase.cat.codes

    cols = df.columns.values
    cols = [*cols[-2:], *cols[:-2]]
    idx = pd.MultiIndex.from_tuples(cols, names=df.columns.names)
    df = df.reindex(columns=idx)
    df.to_csv("puls_phasen.tsv", sep="\t", float_format="%.02f")

    extra = load_group_info()

    df = df.reorder_levels(["run", "prob_nr"], axis=1)
    df = df.T
    df = df.assign(**{c: extra[c] for c in extra.columns})
    df.reset_index().to_csv(
        "puls_alles.tsv", sep="\t", float_format="%.02f", index=False
    )
    df.reset_index(inplace=True)
    df.drop([0, 1], inplace=True)
    idvars = [c for c in df.columns if not isinstance(c, int)]
    lf = df.melt(id_vars=idvars, value_name="puls", var_name="time_point")
    lf["phase"] = phase.cat.codes[lf.time_point].values
    lf.age = lf.age.astype(int)
    runs.reset_index(inplace=True)
    rows = pd.DataFrame(
        data={
            "run": [1, 2],
            "nr": [-1, -1],
            "repetition": [0, 0],
            "condition": ["pause", "pause"],
            "trial_type": ["pause", "pause"],
        }
    )
    runs = pd.concat([runs, rows])
    runs["run_phase"] = runs.nr + (runs.run - 1) * 8
    runs.loc[runs.nr == -1, "run_phase"] = -1
    lf["run_phase"] = lf["run"] * 8 + lf["phase"] - 8
    lf.loc[lf.phase == -1, "run_phase"] = -1
    runs = runs.iloc[:-1, :]
    runs = runs[["run_phase", "repetition", "trial_type", "condition"]]
    runs = runs.set_index("run_phase")
    lf = lf.join(runs, on="run_phase")
    for col in ["run", "age", "run_phase"]:
        lf[col] = lf[col].astype(int)
    lf.to_csv("puls_long.tsv", sep="\t", float_format="%0.2f", index=False)
