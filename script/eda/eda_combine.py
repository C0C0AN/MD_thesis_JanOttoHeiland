"""Füge anhand der Zeiten den Typ des Experiments hinzu.

Block 0: Warten auf Start des Experiments (Pause)
Block 1: Erste Stressphase
Block 2: Pause
Block 3: Musik/Sound
Block 4: Pause
Block 5: Zweite Stressphase
"""
import pandas as pd
from puls_collect import load_group_info, run_intervals, load_runs


def _check_blocks(df):
    probanden = df.prob_id.unique()
    run1 = df[df.block == 1]
    run2 = df[df.block == 5]
    assert {sum(run1.prob_id == p) for p in probanden} <= {723, 724}    
    assert {sum(run2.prob_id == p) for p in probanden} <= {723, 724}    


if __name__ == "__main__":
    df = pd.read_csv("eda_long.tsv", sep="\t")
    probanden = df.prob_id.unique()
    _check_blocks(df)

    df["run"] = -1
    df["phase"] = -2
    df.loc[df.block == 1, "run"] = 1
    df.loc[df.block == 5, "run"] = 2

    intervals = run_intervals()
    for run in [1, 2]:
        for p in probanden:
            mask = (df.run == run) & (df.prob_id == p)
            df.loc[mask, "time"] -= df.loc[mask, "time"].min()
            phase = pd.cut(df.loc[mask, "time"], intervals, labels=False)
            df.loc[mask, "phase"] = phase.cat.codes.astype(int)

    runs = load_runs()
    runs.reset_index(inplace=True)
    runs = runs[["run", "nr", "repetition", "trial_type", "condition"]]
    runs = runs.rename(columns={"nr": "phase"})
    runs = runs.set_index(["run", "phase"])
    lf = df.join(runs, on=["run", "phase"])
    lf.repetition = lf.repetition.fillna(-1).astype(int)
    lf.dropna(inplace=True)

    extra = load_group_info()
    extra.index.set_names(["run", "prob_id"], inplace=True)
    mf = lf.join(extra, on=["run", "prob_id"])
    mf.to_csv("eda_complete.tsv", sep="\t", index=False)
