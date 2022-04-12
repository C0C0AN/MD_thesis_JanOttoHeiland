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
    from os import path

    phasen_tsv = path.join(path.dirname(path.realpath(__file__)), "phasen.tsv")
    runs = load_phasen(phasen_tsv)
    runs["nr"] = list(range(8)) + list(range(8))
    runs = runs.reset_index().set_index(["run", "nr"])
    return runs


def run_intervals(runs=None):
    runs = runs or load_runs()
    # mittlere Start- und End-Zeiten der Phasen
    run = runs.groupby("nr").mean()
    run.repetition = run.repetition.astype(int)
    return pd.IntervalIndex.from_arrays(run.start, run.end)


def combine(df):
    """Lade Phasen-Intervalle und andere Meta-Informationen."""
    probanden = df.prob_id.unique()
    intervals = run_intervals()
    for run in [1, 2]:
        for p in probanden:
            mask = (df.run == run) & (df.prob_id == p)
            df.loc[mask, "time"] -= df.loc[mask, "time"].min()
            phase = pd.cut(df.loc[mask, "time"], intervals, labels=False)
            df.loc[mask, "phase"] = phase.cat.codes.astype(int)

    runs = load_runs()
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
    runs = pd.concat([rows, runs])
    runs = runs[["run", "nr", "repetition", "trial_type", "condition"]]
    runs = runs.rename(columns={"nr": "phase"})
    runs = runs.sort_values(["run", "phase"]).reset_index()
    runs = runs.set_index(["run", "phase"])

    lf = df.join(runs, on=["run", "phase"])
    lf.repetition = lf.repetition.fillna(-1).astype(int)

    extra = load_group_info()
    extra.index.set_names(["run", "prob_id"], inplace=True)
    mf = lf.join(extra, on=["run", "prob_id"])
    mf.sort_values(["run", "time", "prob_id"], inplace=True)
    if "index" in mf.columns:
        mf.drop(columns=["index"], inplace=True)
    mf.dropna(inplace=True)
    mf = mf.astype({"age": int, "repetition": int, "phase": int})
    return mf


def baseline_correction(df, column):
    """Ziehe in Spalte `column` pro Proband den Mittelwert ab."""
    probanden = df["prob_id"].unique()
    for i in probanden:
        mask = df["prob_id"] == i
        df.loc[mask, column] -= df.loc[mask, column].mean()
    df = df.astype({"age": int})
    return df
