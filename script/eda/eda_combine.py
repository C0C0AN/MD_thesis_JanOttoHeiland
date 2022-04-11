"""Füge anhand der Zeiten den Typ des Experiments hinzu.

Block 0: Warten auf Start des Experiments (Pause)
Block 1: Erste Stressphase
Block 2: Pause
Block 3: Musik/Sound
Block 4: Pause
Block 5: Zweite Stressphase
"""
import pandas as pd

from collect import combine


def _check_blocks(df):
    probanden = df.prob_id.unique()
    run1 = df[df.block == 1]
    run2 = df[df.block == 5]
    assert {sum(run1.prob_id == p) for p in probanden} <= {723, 724}
    assert {sum(run2.prob_id == p) for p in probanden} <= {723, 724}


if __name__ == "__main__":
    df = pd.read_csv("eda_long.tsv", sep="\t")
    _check_blocks(df)

    df["run"] = -1
    df["phase"] = -2
    df.loc[df.block == 1, "run"] = 1
    df.loc[df.block == 5, "run"] = 2

    mf = combine(df)
    mf.to_csv("eda_complete.tsv", sep="\t", index=False)
