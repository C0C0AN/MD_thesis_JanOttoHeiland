"""Zusammentragen aller Daten zu den Atmungswerten."""
import pandas as pd
from os import path

from data import HOAF_BIDS


RESP_DIR = f"{HOAF_BIDS}/derivatives/physio/resp"
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
r = pd.concat(dfs)
