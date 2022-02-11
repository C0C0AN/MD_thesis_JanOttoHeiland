"""Analysiere die Start- und Endzeitpunkte der Phasen."""
import pandas as pd


pf = pd.read_csv("phasen.tsv", sep="\t")
idpf = pf.set_index(list(pf.columns[:5]))


def mean_over(index = "prob_nr", pf=pf):
    if isinstance(index, str):
        return mean_over([index], pf=pf)
    assert isinstance(index, list)
    idx = [i for i in pf.index.names if i is not index]
    mf = pf.groupby(idx).mean()
    mf = mf[["start", "end"]]
    return mf
