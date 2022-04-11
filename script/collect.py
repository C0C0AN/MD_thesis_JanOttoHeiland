"""Lade Daten über Gruppenzugehörigkeit, Phasen, etc."""
import pandas as pd


def load_phasen(file_name="phasen.tsv", means=True):
    pf = pd.read_csv(file_name, sep="\t")
    pf = pf.set_index(list(pf.columns[:5]))
    pf = pf.sort_values(["prob_nr", "run", "start"])
    if means:
        return pf.groupby(level=[1, 2, 3, 4], sort=False).mean()
    return pf


def load_group_info():
    """Lade Gruppezugehoerigkeit."""
    from os import path

    from data import HOAF_BIDS

    prob = pd.read_csv(path.join(HOAF_BIDS, "participants.tsv"), sep="\t")
    prob["prob_nr"] = prob.participant_id.str.extract(r"sub-(.+)").astype(int)
    prob = prob.set_index("prob_nr")
    prob = prob.dropna()
    prob = prob.drop(columns=["participant_id"])
    extra = pd.concat((prob, prob), keys=[1, 2])
    extra.index.set_names(["run", "prob_nr"], inplace=True)
    return extra


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
