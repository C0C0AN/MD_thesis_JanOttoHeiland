"""Sammel EDA Daten und schreibe es in CSV Datei."""
import pandas as pd

from blocks import load_blocks
from resp import load_vhdr
from show_eda import DATEN, load_eda

blocks = load_blocks()
keep = blocks.index.str.match(r"HOAF_\d.+vhdr")
blocks.drop(blocks[~keep].index, inplace=True)


def _wip():
    for (prob_id, df) in blocks.iterrows():
        data, times, _ = load_eda(DATEN + "/BekJan/" + prob_id)


if __name__ == "__main__":
    duration = pd.DataFrame(index=blocks.index)
    for i in range(1, 6):
        duration[i] = blocks[i + 1] - blocks[i]
    duration.to_csv("duration.tsv", sep="\t", float_format="%.2f")
