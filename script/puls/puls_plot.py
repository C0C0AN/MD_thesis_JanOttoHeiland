"""Plotte vergleichend Pulsdaten."""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("puls_alles.tsv", sep="\t", index_col=[0, 1])
df = df.set_index(
    pd.MultiIndex.from_tuples(
        [
            ("" if np.isnan(a) else int(a), int(b) if b.isdecimal() else b)
            for a, b in df.index
        ],
        names=df.index.names,
    )
)
