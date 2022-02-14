# coding: utf-8
"""Suche alle Informationen ueber die Pulsdaten zusammen."""
import numpy as np
import pandas as pd
from phases_analyze import load_phasen
from data import DATEN_DIR


def load_runs():
    runs = load_phasen("../phasen.tsv")
    runs['nr'] = list(range(8)) + list(range(8))
    runs = runs.reset_index().set_index(["run", "nr"])
    return runs

file_ma = DATEN_DIR + '/physio_resp_pulse/physio_sub_version/sub_combined.ods'
df = pd.read_excel(file_ma)
# df = df.round(0).astype(int)
df = df[[c for c in df.columns if not c.startswith("Mittelwert")]]
df = df.T
df['run'] = df.index.str.extract(r'.+\:([12])').astype(int).values
df['prob_nr'] = df.index.str.extract(r'[pP](.+):.*').astype(int).values
df = df.reset_index(drop=True).set_index(["prob_nr", "run"])
df = df.T
df['time'] = [i * 1.45 for i in df.index]

runs = load_runs()
run = runs.groupby("nr").mean()
run.repetition = run.repetition.astype(int)

intervals = pd.IntervalIndex.from_arrays(run.start, run.end)
phase = pd.cut(df.time, intervals, labels=False)

df['phase'] = phase.cat.codes

cols = df.columns.values
cols = [*cols[-2:], *cols[:-2]]
idx = pd.MultiIndex.from_tuples(cols, names=df.columns.names)
df = df.reindex(columns=idx)
df.to_csv("puls_phasen.tsv", sep="\t", float_format="%.02f")

# Lade Gruppezugehoerigkeit
from data import HOAF_BIDS
from os import path

prob = pd.read_csv(path.join(HOAF_BIDS, "participants.tsv"), sep="\t")
prob["prob_nr"] = prob.participant_id.str.extract(r"sub-(.+)").astype(int)
prob = prob.set_index("prob_nr")
prob = prob.dropna()
prob = prob.drop(columns=["participant_id"])
extra = pd.concat((prob, prob), keys=[1, 2])
extra.index.set_names(["run", "prob_nr"])

df = df.reorder_levels(["run", "prob_nr"], axis=1)
df = df.T
df = df.assign(**{c: extra[c] for c in extra.columns})
df.reset_index().to_csv("puls_alles.tsv", sep="\t", float_format="%.02f", index=False)
