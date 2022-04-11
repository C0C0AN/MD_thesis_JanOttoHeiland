"""Zusammentragen aller Daten zu den Atmungswerten."""
from os import path

import pandas as pd

from collect import combine
from data import HOAF_BIDS


def concat_all_csvs(RESP_DIR = f"{HOAF_BIDS}/derivatives/physio/resp"):
    """Kombiniere alle Einzelwerte in ein DataFrame."""
    dfs = list()
    for i in range(1, 30):
        for r in [1, 2]:
            csv = f"{RESP_DIR}/sub-{i:02}/sub-{i:02}_task-stress_run-{r}_physio_resp.csv"
            if path.exists(csv):
                d = pd.read_csv(csv, header=None, names=["resp"])
                d["run"] = r
                d["prob_id"] = i
                d.reset_index(inplace=True)
                d["time"] = d["index"] * 1.45
                d.drop(columns=["index"], inplace=True)
                dfs.append(d)

    assert {len(df) for df in dfs} == {500}
    return pd.concat(dfs)


if __name__ == "__main__":
    df = concat_all_csvs()
    mf = combine(df)
    mf["resp"] *= 60
    mf.to_csv("resp_long.tsv", sep="\t", index=False, float_format="%6.2f")
