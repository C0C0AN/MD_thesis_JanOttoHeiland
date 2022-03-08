"""Sammel EDA Daten und schreibe es in CSV Datei."""
import pandas as pd
import numpy as np

from blocks import load_blocks
from show_eda import DATEN, load_eda, compute_reduced_eda

blocks = load_blocks()
keep = blocks.index.str.match(r"HOAF_\d.+vhdr")
blocks.drop(blocks[~keep].index, inplace=True)
blocks[0] = 0.0
blocks = blocks.reindex(columns=range(6))


def _vhdr_filename(prob_id):
    return DATEN + "/BekJan/" + prob_id


def load_reduced_eda() -> list[tuple[np.ndarray, np.ndarray]]:
    """Reduzierte Datenpunkte.

    Für jeden Probanden, `times, data`.
    """
    filenames = [_vhdr_filename(p) for p in blocks.index]
    points_per_sec = 5000
    return compute_reduced_eda(points_per_sec, filenames)


def _wip():
    eda = load_reduced_eda()
    df = pd.DataFrame(data=[e[1] for e in eda], index=blocks.index)
    for i, (prob_id, df) in enumerate(blocks.iterrows()):
        assert (np.gradient(times) > 0).all()  # Prüfe, dass times sortiert
        intervals = pd.IntervalIndex.from_breaks(blocks.loc[prob_id])
        a, b = np.searchsorted(times, [intervals[2].left, intervals[2].right])


if __name__ == "__main__":
    duration = pd.DataFrame(index=blocks.index)
    blocks[0] = 0
    for i in range(6):
        duration[i] = blocks[i + 1] - blocks[i]
    duration.to_csv("duration.tsv", sep="\t", float_format="%.2f")
