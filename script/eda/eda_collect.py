"""Sammel EDA Daten und schreibe es in CSV Datei."""
import numpy as np
import pandas as pd

from blocks import load_blocks
from show_eda import DATEN, compute_reduced_eda


def index_prob_id(blocks):
    """Set prob_id in index."""
    return blocks.set_index(
        pd.Index(
            blocks.index.str.extract(r"HOAF_(\d\d)\.vhdr").astype(int)[0],
            name="prob_id",
        )
    )


def _vhdr_filename(prob_id):
    return f"{DATEN}/BekJan/HOAF_{prob_id:02d}.vhdr"


def load_reduced_eda(prob_ids) -> list[tuple[np.ndarray, np.ndarray]]:
    """Reduzierte Datenpunkte.

    Für jeden Probanden, `times, data`.
    """
    filenames = [_vhdr_filename(p) for p in prob_ids]
    points_per_sec = 5000
    return compute_reduced_eda(points_per_sec, filenames)


def eda_long(blocks) -> pd.DataFrame:
    """Load all EDA data in long format."""
    eda = load_reduced_eda(blocks.index)
    ef = pd.DataFrame(data=[e[1] for e in eda], index=blocks.index)
    lf = (
        ef.reset_index()
        .melt(id_vars=["prob_id"], value_name="eda", var_name="time")
        .dropna()
    )
    lf["block"] = pd.NA
    for i, (pid, breaks) in enumerate(blocks.iterrows()):
        breaks[0] = -0.001
        intervals = pd.IntervalIndex.from_breaks(breaks)
        rows = lf.prob_id == pid
        block_codes = pd.cut(lf.loc[rows, "time"], intervals).cat.codes
        lf.loc[rows, "block"] = block_codes
    lf.block = lf.block.astype("int8")
    return lf


if __name__ == "__main__":
    bs = load_blocks()
    keep = bs.index.str.match(r"HOAF_\d.+vhdr")
    bs.drop(bs[~keep].index, inplace=True)
    bs[0] = 0.0
    bs = bs.reindex(columns=sorted(bs.columns))
    bs.index.set_names("file", inplace=True)

    duration = pd.DataFrame(index=bs.index)
    for i in range(6):
        duration[i] = bs[i + 1] - bs[i]
    duration.to_csv("duration.tsv", sep="\t", float_format="%.2f")

    blocks = index_prob_id(bs)
    lf = eda_long(blocks)
    lf.eda *= 1e6
    lf.to_csv("eda_long.tsv", sep="\t", float_format="%07.4f", index=False)
