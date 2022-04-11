"""Lade Daten über Gruppenzugehörigkeit, Phasen, etc."""
import pandas as pd


def load_group_info():
    """Lade Gruppezugehoerigkeit."""
    from data import HOAF_BIDS
    from os import path

    prob = pd.read_csv(path.join(HOAF_BIDS, "participants.tsv"), sep="\t")
    prob["prob_nr"] = prob.participant_id.str.extract(r"sub-(.+)").astype(int)
    prob = prob.set_index("prob_nr")
    prob = prob.dropna()
    prob = prob.drop(columns=["participant_id"])
    extra = pd.concat((prob, prob), keys=[1, 2])
    extra.index.set_names(["run", "prob_nr"], inplace=True)
    return extra
